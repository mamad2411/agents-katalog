---
description: Standards for implementing Hotwire (Turbo and Stimulus.js) in Rails applications
globs:
  - "app/javascript/controllers/**/*.js"
  - "app/views/**/*.erb"
  - "app/controllers/**/*.rb"
---
# Hotwire Implementation Standards

<rule>
name: hotwire_standards
description: Standards for implementing Hotwire, including Turbo and Stimulus.js patterns

filters:
  - type: file_extension
    pattern: "\\.js$|\\.erb$|\\.rb$"
  - type: content
    pattern: "data-controller|turbo_frame_tag|turbo_stream|stimulus|@hotwired"

actions:
  - type: suggest
    message: |
      When implementing Hotwire features:

      1. Turbo Frame Patterns:
         ```erb
         <%# Basic Turbo Frame %>
         <%= turbo_frame_tag "content" do %>
           <%= render "shared/content" %>
         <% end %>

         <%# Lazy Loading Frame %>
         <%= turbo_frame_tag "lazy_content",
             src: load_content_path,
             loading: :lazy do %>
           <%= render "shared/loading" %>
         <% end %>

         <%# Target Navigation %>
         <%= link_to "Edit",
             edit_resource_path(@resource),
             data: { turbo_frame: "content" } %>
         ```

      2. Turbo Stream Responses:
         ```ruby
         # Controller Action
         def create
           @resource = Resource.new(resource_params)
           
           if @resource.save
             respond_to do |format|
               format.turbo_stream
               format.html { redirect_to @resource }
             end
           else
             render :new, status: :unprocessable_entity
           end
         end

         # View Template (create.turbo_stream.erb)
         <%= turbo_stream.append "resources", @resource %>
         <%= turbo_stream.update "new_resource",
             partial: "form",
             locals: { resource: Resource.new } %>
         <%= turbo_stream.update "flash",
             partial: "shared/flash",
             locals: { message: "Created successfully" } %>
         ```

      3. Stimulus Controller Patterns:
         ```javascript
         // Basic Controller (controllers/example_controller.js)
         import { Controller } from "@hotwired/stimulus"

         export default class extends Controller {
           static targets = ["output"]
           static values = {
             url: String,
             refreshInterval: { type: Number, default: 5000 }
           }

           connect() {
             if (this.hasRefreshIntervalValue) {
               this.startRefreshing()
             }
           }

           disconnect() {
             if (this.refreshTimer) {
               clearInterval(this.refreshTimer)
             }
           }

           startRefreshing() {
             this.refreshTimer = setInterval(() => {
               this.refresh()
             }, this.refreshIntervalValue)
           }

           async refresh() {
             try {
               const response = await fetch(this.urlValue)
               if (response.ok) {
                 const html = await response.text()
                 this.outputTarget.innerHTML = html
               }
             } catch (error) {
               console.error("Failed to refresh:", error)
             }
           }
         }
         ```

      4. Form Submissions:
         ```erb
         <%= form_with(model: @resource, data: { controller: "form" }) do |form| %>
           <div data-form-target="fields">
             <%= form.text_field :name,
                 data: {
                   form_target: "input",
                   action: "input->form#validate"
                 } %>
           </div>

           <div data-form-target="errors"></div>

           <%= form.submit data: { action: "form#submit" } %>
         <% end %>

         <%# Corresponding Stimulus Controller %>
         // controllers/form_controller.js
         import { Controller } from "@hotwired/stimulus"

         export default class extends Controller {
           static targets = ["input", "errors"]

           validate(event) {
             const input = event.target
             // Implement validation logic
           }

           async submit(event) {
             event.preventDefault()
             // Handle form submission
           }
         }
         ```

      5. Real-time Updates:
         ```ruby
         # Model Broadcasting
         class Comment < ApplicationRecord
           after_create_commit -> {
             broadcast_append_to "comments",
             partial: "comments/comment",
             locals: { comment: self }
           }
         end

         # View Subscription
         <%= turbo_stream_from "comments" %>
         <div id="comments">
           <%= render @comments %>
         </div>
         ```

      6. Stimulus Values and Classes:
         ```erb
         <div data-controller="toggle"
              data-toggle-active-class="bg-blue-500"
              data-toggle-url-value="/api/toggle"
              data-toggle-id-value="123">
           <button data-action="toggle#toggle">Toggle</button>
         </div>

         // controllers/toggle_controller.js
         import { Controller } from "@hotwired/stimulus"

         export default class extends Controller {
           static values = {
             active: Boolean,
             url: String,
             id: String
           }
           static classes = ["active"]

           toggle() {
             this.activeValue = !this.activeValue
             this.element.classList.toggle(this.activeClass)
           }
         }
         ```

      7. Turbo Progress Bar:
         ```javascript
         // config/importmap.rb
         pin "@hotwired/turbo-rails", to: "turbo.min.js"

         // app/javascript/application.js
         import "@hotwired/turbo-rails"

         Turbo.setProgressBarDelay(100)
         ```

examples:
  - input: |
      # Bad - Direct DOM manipulation
      document.getElementById("content").innerHTML = "New content"
      
      # Good - Using Turbo Stream
      <%= turbo_stream.update "content", "New content" %>
    output: "Using Turbo Stream for DOM updates"

  - input: |
      # Bad - jQuery-style code
      $(document).on("click", ".button", function() {
        $.ajax(...)
      })
      
      # Good - Stimulus controller
      import { Controller } from "@hotwired/stimulus"
      
      export default class extends Controller {
        static targets = ["button"]
        
        click() {
          // Handle click with Stimulus
        }
      }
    output: "Using Stimulus for JavaScript interactions"

metadata:
  priority: high
  version: 1.0
  related_rules:
    - ui_styling
    - ux_standards
  responsibility: "Hotwire implementation patterns"
  standard_patterns:
    turbo:
      - frames
      - streams
      - progress_bar
    stimulus:
      - controllers
      - targets
      - values
      - actions
</rule>