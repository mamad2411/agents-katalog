---
description: Standards for ensuring a positive user experience
globs: 
---

# UX Standards

<rule>
name: ux_standards
description: Standards for implementing a positive user experience through effective design patterns and interactions following Rails conventions

filters:
  - type: file_extension
    pattern: "\\.rb$|\\.erb$|\\.js$"
  - type: content
    pattern: "class=|render|redirect_to|form_with|link_to|button_to"

actions:
  - type: suggest
    message: |
      When designing for UX:

      1. Navigation and Information Architecture:
         - Implement clear, consistent navigation patterns
         - Use breadcrumbs for deep navigation
         - Organize content logically and intuitively
         ```erb
         <%# Clear navigation structure %>
         <%= render "shared/navigation" do %>
           <%= render "shared/nav_item", 
               title: t(".dashboard"),
               path: dashboard_path,
               active: current_page?(dashboard_path) %>
         <% end %>
         ```

      2. User Feedback and States:
         - Use Rails flash messages for feedback
         - Leverage Turbo Stream for dynamic updates
         - Implement progress indicators with Turbo
         ```erb
         <%# Feedback using Rails conventions %>
         <%= render "shared/flash_messages" %>
         
         <%# Turbo Frame with loading state %>
         <%= turbo_frame_tag "content" do %>
           <%= render "shared/loading_indicator" if @loading %>
           <%= render @content unless @loading %>
         <% end %>
         ```

      3. Form Design and Validation:
         - Use Rails form helpers with model validations
         - Show inline errors with form object
         - Leverage Rails form builder
         ```erb
         <%= form_with(model: @user) do |form| %>
           <div class="field">
             <%= form.label :email %>
             <%= form.email_field :email, class: "form-input" %>
             <%= form.error_messages_for :email %>
           </div>

           <div class="actions">
             <%= form.submit class: "btn btn-primary" %>
           </div>
         <% end %>
         ```

      4. Content Hierarchy:
         - Use semantic HTML with Rails helpers
         - Implement proper heading structure
         - Highlight important actions
         ```erb
         <div class="content-section">
           <header class="mb-4">
             <h1 class="h2"><%= t(".title") %></h1>
             <p class="text-gray-600"><%= t(".description") %></p>
           </header>

           <div class="actions mb-4">
             <%= link_to t(".new_resource"),
                 new_resource_path,
                 class: "btn btn-primary" %>
           </div>

           <div class="resources">
             <%= render @resources %>
           </div>
         </div>
         ```

      5. Interaction Design:
         - Use Rails UJS for enhanced interactions
         - Implement Turbo Drive for navigation
         - Provide clear hover/active states
         ```erb
         <%# Resource actions with Rails UJS %>
         <%= button_to resource_path(resource),
             method: :delete,
             class: "btn btn-danger",
             data: { 
               turbo_confirm: t(".confirm_delete")
             } do %>
           <%= t(".delete") %>
         <% end %>
         ```

      6. Progressive Enhancement:
         - Use Turbo Frames for partial updates
         - Implement Turbo Streams for real-time
         - Provide non-JS fallbacks
         ```erb
         <%# Progressive loading with Turbo %>
         <%= turbo_frame_tag "items" do %>
           <%= render @items %>
           <%= turbo_frame_tag "loading_more",
               src: next_page_path,
               loading: :lazy if @pagy.next %>
         <% end %>
         ```

      7. Error Handling:
         - Use Rails error pages and rescues
         - Implement proper status codes
         - Show user-friendly messages
         ```erb
         <%# Error handling in views %>
         <% if resource.errors.any? %>
           <div class="error-messages" role="alert">
             <h2><%= t(".error_message", count: resource.errors.count) %></h2>
             <ul>
               <% resource.errors.full_messages.each do |message| %>
                 <li><%= message %></li>
               <% end %>
             </ul>
           </div>
         <% end %>
         ```

      8. Responsive Behavior:
         - Use Tailwind's responsive classes
         - Implement mobile-first design
         - Support different viewport sizes
         ```erb
         <div class="container mx-auto px-4">
           <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
             <%= render partial: "card", collection: @items %>
           </div>
         </div>
         ```

examples:
  - input: |
      # Bad - Non-Rails form implementation
      <form>
        <input type="text">
        <button>Submit</button>
      </form>
      
      # Good - Rails form with proper feedback
      <%= form_with(model: @resource) do |form| %>
        <div class="field">
          <%= form.label :name %>
          <%= form.text_field :name, class: "form-input" %>
          <%= form.error_messages_for :name %>
        </div>

        <div class="actions">
          <%= form.submit class: "btn btn-primary" %>
        </div>
      <% end %>
    output: "Using Rails form helpers with proper error handling"

  - input: |
      # Bad - Direct HTML without Rails helpers
      <div>
        <h1>Resources</h1>
        <a href="/resources/new">New Resource</a>
        <div class="items">
          <!-- Items here -->
        </div>
      </div>
      
      # Good - Rails helpers and conventions
      <div class="container">
        <header class="mb-4">
          <h1 class="h2"><%= t(".resources") %></h1>
          <%= link_to t(".new_resource"),
              new_resource_path,
              class: "btn btn-primary" %>
        </header>

        <%= turbo_frame_tag "resources" do %>
          <%= render @resources %>
        <% end %>
      </div>
    output: "Using Rails helpers and conventions for better UX"

metadata:
  priority: high
  version: 1.0
  related_rules:
    - ui_styling
  responsibility: "Ensuring a positive user experience following Rails conventions"
  standard_patterns:
    feedback:
      - flash_messages
      - form_errors
      - turbo_streams
    navigation:
      - link_to
      - button_to
      - turbo_frame_tag
    forms:
      - form_with
      - error_messages_for
      - field_with_errors
</rule>