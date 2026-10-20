---
description: Index of Rails-specific Cursor rules for standard Rails applications using Hotwire and Stimulus.js
globs: ["**/*.{rb,js,erb}"]
---

# Rails Cursor Rules Index

This index organizes the essential Cursor rules for a standard Rails application using Hotwire and Stimulus.js.

## Core Framework Rules

1. **Model Standards**
   - solid_principles.mdc
   - Active Record patterns and validations
   - Standard Rails callbacks
   - Basic model organization

2. **Controller Standards**
   - Standard RESTful actions
   - Basic before_actions
   - Standard Rails responses
   - Turbo Stream responses

3. **View Standards**
   - ui_styling.mdc (Tailwind implementation)
   - ux_standards.mdc (Rails UX patterns)
   - accessibility_standards.mdc
   - Standard Rails form helpers
   - Turbo Frame patterns

## Hotwire Integration

1. **Turbo Patterns**
   - Turbo Frame usage
   - Turbo Stream responses
   - Turbo Drive configuration
   - Form submissions
   - List updates

2. **Stimulus.js Standards**
   - Controller naming
   - Action definitions
   - Target usage
   - Value definitions
   - Standard controller patterns

## Testing Standards

1. **RSpec Implementation**
   - testing_standards.mdc
   - Model specs
   - Controller specs
   - System tests with Turbo
   - Stimulus.js interaction testing

## Notification System

1. **Noticed Integration**
   - noticed_notification_standards.mdc
   - Standard notification patterns
   - Database delivery
   - Email delivery

## Mailer Standards

1. **Mail Implementation**
   - mailer_html_file_compliance.mdc
   - mailer_text_file_compliance.mdc
   - Standard mailer patterns
   - Multipart emails

## Database Standards

1. **Schema Design**
   - database_patterns.mdc
   - Standard Rails migrations
   - Index usage
   - Foreign key constraints

## Documentation

1. **Code Documentation**
   - documentation_guideline.mdc
   - YARD documentation
   - README standards
   - API documentation

## Rules to Skip/Avoid

1. **Unnecessary Complexity**
   - Service objects (use standard Rails patterns instead)
   - Complex presenter patterns
   - Repository patterns
   - Additional architectural layers beyond MVC

## Standard Rails Conventions to Follow

1. **Model Layer**
   ```ruby
   class Post < ApplicationRecord
     belongs_to :user
     has_many :comments
     
     validates :title, presence: true
     validates :content, presence: true
     
     scope :published, -> { where(published: true) }
   end
   ```

2. **Controller Layer**
   ```ruby
   class PostsController < ApplicationController
     before_action :set_post, only: [:show, :edit, :update, :destroy]
     
     def index
       @posts = Post.published
     end
     
     def create
       @post = Post.new(post_params)
       
       if @post.save
         respond_to do |format|
           format.html { redirect_to @post }
           format.turbo_stream
         end
       else
         render :new, status: :unprocessable_entity
       end
     end
   end
   ```

3. **View Layer with Turbo**
   ```erb
   <%= turbo_frame_tag "posts" do %>
     <%= render @posts %>
     
     <%= turbo_frame_tag "new_post" do %>
       <%= render "form", post: @post %>
     <% end %>
   <% end %>
   ```

4. **Stimulus Controller**
   ```javascript
   // app/javascript/controllers/form_controller.js
   import { Controller } from "@hotwired/stimulus"

   export default class extends Controller {
     static targets = [ "input", "output" ]
     
     connect() {
       // Standard initialization
     }
     
     submit(event) {
       // Standard form handling
     }
   }
   ```

## Implementation Notes

1. Follow standard Rails conventions first
2. Use Hotwire's Turbo for most dynamic updates
3. Use Stimulus.js for client-side interactions only when needed
4. Keep controllers RESTful
5. Use standard Active Record patterns
6. Leverage Rails' built-in testing tools
7. Follow standard Rails directory structure

## Related Documentation

- [Rails Guides](https://guides.rubyonrails.org/)
- [Hotwire](https://hotwired.dev/)
- [Stimulus.js](https://stimulus.hotwired.dev/)
- [Turbo Handbook](https://turbo.hotwired.dev/handbook/introduction)