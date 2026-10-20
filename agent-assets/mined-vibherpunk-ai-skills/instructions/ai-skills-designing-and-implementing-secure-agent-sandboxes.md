# Copilot Instructions: Designing And Implementing Secure Agent Sandboxes
Description: This skill provides a comprehensive guide for designing and implementing secure agent sandboxes, focusing on running untrusted code securely and reliably at scale. It covers core concepts, detailed workflows, best practices, common pitfalls, and validation steps.

### Overview

Agent sandboxes are essential for securely executing untrusted code, especially in AI-driven environments like ChatGPT and Codex. This skill covers the design and implementation of secure sandboxes, focusing on runtime security, persistence, and orchestration. The core concepts include understanding sandbox isolation, the role of containers and microVMs, and the importance of persistence for reliability and scalability.

### Step-by-Step Workflow

1. **Understand the Need for Sandboxes**: Recognize the necessity of sandboxes for running untrusted code securely. Learn why traditional methods like `fork` and `exec` are insufficient due to security vulnerabilities.

2. **Choose the Right Isolation Mechanism**: Decide between containers and microVMs based on your security and performance needs. Containers offer resource isolation but still share the host kernel, while microVMs provide hardware-level isolation.

3. **Implement MicroVM-Based Sandboxes**: Use microVMs for enhanced security. Follow these steps:
   - Fork a Cloud Hypervisor binary process.
   - Expose an API over a Unix domain socket.
   - Call the `create` API to set up the root FS, kernel, CPU, and memory.
   - Start the microVM.

4. **Enable Persistence**: Implement disk persistence to ensure data durability across sandbox sessions. Use incremental snapshotting to efficiently save and restore sandbox states.

5. **Orchestrate Sandboxes Across Nodes**: Use a control plane to manage sandboxes across multiple nodes. Implement a scheduler to route sandboxes based on load and region.

### Code Snippets

```bash
# Example: Starting a MicroVM with Cloud Hypervisor
cloud-hypervisor --api-socket /tmp/ch.sock &
curl -X POST --unix-socket /tmp/ch.sock -d '{"kernel": "/path/to/kernel", "rootfs": "/path/to/rootfs", "cpu": 2, "memory": 2048}' http://localhost/create
curl -X POST --unix-socket /tmp/ch.sock http://localhost/start
```

### Best Practices

- **Security First**: Always prioritize security over performance. Use microVMs for hardware-level isolation.
- **Incremental Snapshotting**: Implement incremental snapshotting to save only the changes between snapshots, reducing storage and latency.
- **Low Latency Creation**: Pre-warm sandboxes or use memory snapshots to achieve low latency creation.

### Common Pitfalls

- **Noisy Neighbors**: Avoid using `fork` and `exec` directly, as they can lead to noisy neighbor issues, where one sandbox consumes all resources.
- **Kernel Exploits**: Be aware that containers still share the host kernel, making them vulnerable to kernel exploits.
- **Performance Overheads**: Understand the performance trade-offs with microVMs, especially when switching between guest and host contexts.

### Validation and Testing

- **Security Testing**: Regularly test sandboxes for vulnerabilities, including kernel exploits and privilege escalation.
- **Performance Testing**: Measure the latency and throughput of sandbox creation and execution to ensure they meet product requirements.
- **Persistence Testing**: Verify that snapshots are correctly saved and restored, ensuring data durability across sessions.

### References

For more detailed information, refer to the following documents:

- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

### Code Examples

This document provides concrete code snippets for implementing secure agent sandboxes.

#### Starting a MicroVM with Cloud Hypervisor

```bash
# Fork the Cloud Hypervisor binary process
cloud-hypervisor --api-socket /tmp/ch.sock &

# Call the create API to set up the root FS, kernel, CPU, and memory
curl -X POST --unix-socket /tmp/ch.sock -d '{"kernel": "/path/to/kernel", "rootfs": "/path/to/rootfs", "cpu": 2, "memory": 2048}' http://localhost/create

# Start the microVM
curl -X POST --unix-socket /tmp/ch.sock http://localhost/start
```

#### Incremental Snapshotting

```bash
# Example: Creating an incremental snapshot
# Identify changed blocks using FIE map
fiemap --file /path/to/file --output /path/to/changed_blocks

# Zip the changed blocks and upload to cloud storage
zip -r /path/to/snapshot.zip /path/to/changed_blocks
scp /path/to/snapshot.zip user@cloud:/path/to/destination
```

For more detailed information, refer to the [Practical Guide](references/practical_guide.md) and [Common Pitfalls](references/common_pitfalls.md).

### Common Pitfalls

### Common Pitfalls

This document outlines common pitfalls when designing and implementing secure agent sandboxes.

#### Noisy Neighbors

Using `fork` and `exec` directly can lead to noisy neighbor issues, where one sandbox consumes all resources, bringing down the entire node.

#### Kernel Exploits

Containers still share the host kernel, making them vulnerable to kernel exploits. Always prefer microVMs for hardware-level isolation.

#### Performance Overheads

MicroVMs introduce performance overheads, especially when switching between guest and host contexts. Be aware of these trade-offs and optimize accordingly.

#### Security Testing

Regularly test sandboxes for vulnerabilities, including kernel exploits and privilege escalation. Ensure that your sandboxes are secure before deploying them in production.

#### Persistence Testing

Verify that snapshots are correctly saved and restored, ensuring data durability across sessions. Implement incremental snapshotting to reduce storage and latency.

For more detailed information, refer to the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Core Concepts

### Core Concepts

Agent sandboxes are isolated environments designed to securely execute untrusted code. They are crucial in AI-driven applications like ChatGPT and Codex, where models may generate and execute code to solve tasks. The primary goal of a sandbox is to ensure that the executed code cannot exploit vulnerabilities in the host system or access unauthorized data.

#### Isolation Mechanisms

- **Containers**: Use namespaces and cgroups to isolate resources. While containers provide some level of isolation, they still share the host kernel, making them vulnerable to kernel exploits.
- **MicroVMs**: Provide hardware-level isolation by running a separate Linux kernel in a virtual machine. This ensures that even if the guest kernel is compromised, the host remains secure.

#### Persistence

Persistence is essential for maintaining state across sandbox sessions. Incremental snapshotting allows efficient saving and restoring of sandbox states, ensuring data durability and reliability.

#### Orchestration

Orchestration involves managing sandboxes across multiple nodes in a cloud environment. A control plane and scheduler are used to route sandboxes based on load and region, ensuring low latency and high reliability.

For more detailed information, refer to the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

### Practical Guide

### Practical Guide

This guide provides step-by-step instructions for implementing secure agent sandboxes, focusing on microVMs and persistence.

#### Step 1: Understand the Need for Sandboxes

Sandboxes are necessary for securely executing untrusted code. Traditional methods like `fork` and `exec` are insufficient due to security vulnerabilities.

#### Step 2: Choose the Right Isolation Mechanism

Decide between containers and microVMs based on your security and performance needs. Containers offer resource isolation but still share the host kernel, while microVMs provide hardware-level isolation.

#### Step 3: Implement MicroVM-Based Sandboxes

Use microVMs for enhanced security. Follow these steps:

1. Fork a Cloud Hypervisor binary process.
2. Expose an API over a Unix domain socket.
3. Call the `create` API to set up the root FS, kernel, CPU, and memory.
4. Start the microVM.

#### Step 4: Enable Persistence

Implement disk persistence to ensure data durability across sandbox sessions. Use incremental snapshotting to efficiently save and restore sandbox states.

#### Step 5: Orchestrate Sandboxes Across Nodes

Use a control plane to manage sandboxes across multiple nodes. Implement a scheduler to route sandboxes based on load and region.

For more detailed information, refer to the [Core Concepts](references/core_concepts.md) and [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[From fork() to Fleet: Designing an Agent Sandbox Cloud — Abhishek Bhardwaj, OpenAI](https://www.youtube.com/watch?v=OqM67QG_Ikk)** by AI Engineer