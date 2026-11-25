---
name: multicore-vulkan
description: Multi-core Vulkan rendering workflow with synchronization, frames in flight, and per-thread command pools. Use when implementing the render loop, managing Vulkan synchronization, handling frames in flight, setting up command pools for multi-threading, or when the user asks about fences, semaphores, barriers, swapchain sync, or GPU/CPU coordination.
---

# Multi-Core Vulkan Rendering Workflow

You are an expert in combining lane-based multi-core architecture with Vulkan rendering. When helping with the render pipeline, follow these principles strictly.

## Core Principle

**CPU lanes and GPU synchronization solve two entirely different timeline problems.**

- `lane_sync()` / barriers → sync CPU threads with each other
- Vulkan fences → sync CPU with GPU (prevent overwriting in-flight data)
- Vulkan semaphores → sync GPU with GPU (internal pipeline ordering)
- Pipeline barriers → sync GPU memory/layout transitions

Never confuse these. Never use Vulkan sync primitives to coordinate CPU threads.

## Frames in Flight & Buffer Double/Triple Buffering

To prevent CPU stalls waiting for the GPU:

- Run 2-3 frames in flight simultaneously
- **Double/triple-buffer all dynamic CPU-to-GPU data**: ObjectBuffer, IndirectDrawBuffer
- While GPU renders Frame 0's buffers, CPU lanes safely pack Frame 1's buffers lock-free
- Each frame index has its own copy of dynamic buffers

```
// 3 frames in flight = 3 copies of each dynamic buffer
object_buffers:   [MAX_FRAMES_IN_FLIGHT]Mapped_Buffer
indirect_buffers: [MAX_FRAMES_IN_FLIGHT]Mapped_Buffer
```

## Per-Thread Command Pools

**VkCommandPool is NOT thread-safe.** Multiple lanes cannot allocate from the same pool.

Allocate pools based on `frames_in_flight * core_count`:

```
// Allocated at engine startup
command_pools:   [MAX_FRAMES_IN_FLIGHT][NUMBER_OF_CORES]vk.CommandPool
command_buffers: [MAX_FRAMES_IN_FLIGHT][NUMBER_OF_CORES]vk.CommandBuffer
```

Each lane indexes by `[current_frame][lane_idx()]` — guaranteed unique, zero contention.

## The Frame Workflow

### Phase 1: Go Wide (All Lanes)

All CPU lanes execute the same rendering function. Each lane:

1. Gets its chunk via `lane_range(active_entity_count)`
2. Writes transforms/materials into `mapped_object_buffer[current_frame]` at its offset
3. Writes draw commands into `mapped_indirect_buffer[current_frame]` at its offset
4. (Optional) Records secondary command buffers from `command_pools[current_frame][lane_idx()]`

All writes are lock-free — offsets are mathematically non-overlapping.

### Phase 2: Synchronize

```
lane_sync()  // Wait for ALL lanes to finish packing buffers
```

### Phase 3: Go Narrow (Lane 0 Only)

Lane 0 handles all Vulkan API interaction:

```
if lane_idx() == 0 {
    // 1. Wait for GPU to finish with THIS frame's resources
    vk.WaitForFences(device, 1, &frame_fences[current_frame], true, max(u64))
    vk.ResetFences(device, 1, &frame_fences[current_frame])

    // 2. Acquire swapchain image (signals image_available_semaphore)
    image_index: u32
    vk.AcquireNextImageKHR(device, swapchain, max(u64),
        image_available_semaphores[current_frame], {}, &image_index)

    // 3. Record primary command buffer
    //    - Bind uber pipeline + global descriptor set
    //    - vkCmdDrawIndirect with the packed indirect buffer
    cmd := record_frame_commands(current_frame, image_index)

    // 4. Submit (wait on image_available, signal render_finished)
    submit_info := vk.SubmitInfo {
        waitSemaphoreCount   = 1,
        pWaitSemaphores      = &image_available_semaphores[current_frame],
        commandBufferCount   = 1,
        pCommandBuffers      = &cmd,
        signalSemaphoreCount = 1,
        pSignalSemaphores    = &render_finished_semaphores[current_frame],
    }
    vk.QueueSubmit(graphics_queue, 1, &submit_info, frame_fences[current_frame])

    // 5. Present (wait on render_finished)
    present_info := vk.PresentInfoKHR {
        waitSemaphoreCount = 1,
        pWaitSemaphores    = &render_finished_semaphores[current_frame],
        swapchainCount     = 1,
        pSwapchains        = &swapchain,
        pImageIndices       = &image_index,
    }
    vk.QueuePresentKHR(present_queue, &present_info)
}
```

### Phase 4: Final Sync

```
lane_sync()  // No lane advances to next frame until submission is done
current_frame = (current_frame + 1) % MAX_FRAMES_IN_FLIGHT
```

## Synchronization Primitives Summary

| Primitive | Timeline | Purpose |
|---|---|---|
| `lane_sync()` | CPU ↔ CPU | Wait for all lanes to finish a phase |
| `VkFence` | CPU ↔ GPU | Prevent CPU from overwriting in-flight frame data |
| `VkSemaphore` (image_available) | GPU ↔ GPU | Swapchain image is ready for rendering |
| `VkSemaphore` (render_finished) | GPU ↔ GPU | Rendering is done, safe to present |
| `VkPipelineBarrier` | GPU internal | Memory/layout transitions (e.g., UNDEFINED → COLOR_ATTACHMENT) |

## Dynamic Rendering (Vulkan 1.3)

**Never create VkRenderPass or VkFramebuffer objects.** Use dynamic rendering exclusively.

Instead of baking render targets into static objects, pass attachments directly to the command buffer:

```
// In go-narrow phase, after acquiring swapchain image:
color_attachment := vk.RenderingAttachmentInfo {
    sType       = .RENDERING_ATTACHMENT_INFO,
    imageView   = swapchain_image_views[image_index],
    imageLayout = .COLOR_ATTACHMENT_OPTIMAL,
    loadOp      = .CLEAR,
    storeOp     = .STORE,
    clearValue  = { color = { float32 = {0.1, 0.1, 0.1, 1.0} } },
}
depth_attachment := vk.RenderingAttachmentInfo {
    sType       = .RENDERING_ATTACHMENT_INFO,
    imageView   = depth_image_view,
    imageLayout = .DEPTH_STENCIL_ATTACHMENT_OPTIMAL,
    loadOp      = .CLEAR,
    storeOp     = .DONT_CARE,
    clearValue  = { depthStencil = { depth = 1.0 } },
}
render_info := vk.RenderingInfo {
    sType                = .RENDERING_INFO,
    renderArea           = { extent = { width, height } },
    layerCount           = 1,
    colorAttachmentCount = 1,
    pColorAttachments    = &color_attachment,
    pDepthAttachment     = &depth_attachment,
}
vk.CmdBeginRendering(cmd, &render_info)
// ... bind pipeline, descriptor sets, draw ...
vk.CmdEndRendering(cmd)
```

### Pipeline Creation Without VkRenderPass

Set `renderPass = VK_NULL_HANDLE` and chain a `VkPipelineRenderingCreateInfo`:

```
pipeline_rendering_info := vk.PipelineRenderingCreateInfo {
    sType                   = .PIPELINE_RENDERING_CREATE_INFO,
    colorAttachmentCount    = 1,
    pColorAttachmentFormats = &swapchain_format,
    depthAttachmentFormat   = depth_format,
}
pipeline_info := vk.GraphicsPipelineCreateInfo {
    // ... stages, viewport, rasterization, etc ...
    renderPass = vk.RenderPass(0), // VK_NULL_HANDLE
    pNext      = &pipeline_rendering_info,
}
```

### Required Image Layout Transitions

Before beginning dynamic rendering, transition the swapchain image layout with pipeline barriers:

```
// UNDEFINED → COLOR_ATTACHMENT_OPTIMAL before rendering
// COLOR_ATTACHMENT_OPTIMAL → PRESENT_SRC_KHR after rendering
```

## Secondary Command Buffers (Alternative)

If rendering is too complex for a single indirect draw, record Vulkan commands in parallel across lanes.

With dynamic rendering, secondary buffers inherit attachment *formats* (not a VkRenderPass object):

```
// Go Wide: each lane sets up inheritance and records
inheritance_rendering := vk.CommandBufferInheritanceRenderingInfo {
    sType                   = .COMMAND_BUFFER_INHERITANCE_RENDERING_INFO,
    colorAttachmentCount    = 1,
    pColorAttachmentFormats = &swapchain_format,
    depthAttachmentFormat   = depth_format,
    rasterizationSamples    = {._1},
}
inheritance_info := vk.CommandBufferInheritanceInfo {
    sType = .COMMAND_BUFFER_INHERITANCE_INFO,
    pNext = &inheritance_rendering,
}
begin_info := vk.CommandBufferBeginInfo {
    sType = .COMMAND_BUFFER_BEGIN_INFO,
    flags = { .RENDER_PASS_CONTINUE, .ONE_TIME_SUBMIT },
    pInheritanceInfo = &inheritance_info,
}
secondary_cmd := command_buffers[current_frame][lane_idx()]
vk.BeginCommandBuffer(secondary_cmd, &begin_info)
// ... lane-specific draw calls ...
vk.EndCommandBuffer(secondary_cmd)

lane_sync()

// Go Narrow: Lane 0 executes all secondaries
if lane_idx() == 0 {
    // Begin primary, begin dynamic rendering, then:
    vk.CmdExecuteCommands(primary_cmd, u32(core_count), &secondary_cmds[0])
    vk.CmdEndRendering(primary_cmd)
}
```

- **Go Wide**: Each lane records a `VK_COMMAND_BUFFER_LEVEL_SECONDARY` from its own pool
- **Go Narrow**: Lane 0 calls `vkCmdExecuteCommands` to bundle all secondary buffers into one primary
- Still one submission to the graphics queue

## Async Asset Loading

Dedicate specific lanes to disk I/O:

1. Background lane loads texture from disk into a staging buffer
2. Records a transfer command on a dedicated **transfer queue**
3. Uses a VkFence to signal completion
4. Main graphics lane waits on the fence before sampling the new texture

## Rules When Writing Vulkan Multi-Core Code

- Never share a VkCommandPool across threads — one pool per lane per frame
- Never use Vulkan fences/semaphores for CPU thread sync — use `lane_sync()`
- Always double/triple-buffer dynamic Vulkan buffers per frame in flight
- Always wait on frame fence before reusing that frame's resources
- Swapchain acquire → wait semaphore before rendering; render done → signal semaphore before present
- Only Lane 0 talks to the Vulkan driver for submission and presentation
- Never create VkRenderPass or VkFramebuffer — use dynamic rendering exclusively
- Always transition image layouts via pipeline barriers before/after `vkCmdBeginRendering`
- Set `renderPass = VK_NULL_HANDLE` in pipeline creation; use `VkPipelineRenderingCreateInfo` instead

## Anti-Patterns (Never Do This)

- Never let multiple lanes submit to the same queue without serialization
- Never reuse a frame's buffers before its fence signals
- Never map/unmap buffers per frame — keep them persistently mapped
- Never use mutexes to protect Vulkan command recording — use per-lane pools
- Never record all commands on a single thread — go wide with secondary buffers or parallel indirect generation
- Never create VkRenderPass or VkFramebuffer objects — they are obsolete in Vulkan 1.3
- Never pass a VkRenderPass to secondary command buffer inheritance — use `VkCommandBufferInheritanceRenderingInfo`
