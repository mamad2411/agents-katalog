---
description: Ensures Rails controllers follow RESTful conventions, proper filter usage, and secure parameter management.
globs:
  - "app/controllers/**/*.rb"
---

# Controllers

<rule>
name: controllers_standard
description: Enforces conventions for Rails controllers including RESTful actions, proper filters, secure parameter handling, and clear separation of concerns.

filters:
  - type: path
    pattern: "^app/controllers/.*\\.rb$"
    # Applies to all controller files in the app/controllers directory

actions:
  - type: suggest
    message: |
      Controllers should:
      1. Follow RESTful conventions (e.g., index, show, create, update, destroy).
      2. Use before_action filters for authentication and parameter sanitization.
      3. Keep actions concise; delegate complex logic to models or helpers.
      4. Handle errors gracefully and return meaningful responses.
      5. Avoid embedding business logic directly within controller actions.

examples:
  - input: |
      # Bad example: Controller with mixed responsibilities and missing filters
      class UsersController < ApplicationController
        def create
          user = User.new(params[:user])
          if user.save
            # processing
          else
            # error handling
          end
        end
      end
    output: "Controller should use strong parameters and before_action filters for clarity and security."
  - input: |
      # Good example
      class UsersController < ApplicationController
        before_action :set_user, only: [:show, :update, :destroy]
        before_action :authenticate_user!

        def create
          @user = User.new(user_params)
          if @user.save
            render json: @user, status: :created
          else
            render json: @user.errors, status: :unprocessable_entity
          end
        end

        private

        def set_user
          @user = User.find(params[:id])
        end

        def user_params
          params.require(:user).permit(:name, :email, :password)
        end
      end
    output: "Controller properly applies filters, uses strong parameters, and follows RESTful design."

metadata:
  priority: high
  version: 1.0
  related_rules:
    - rails_project
  responsibility: "Ensure Rails controllers adhere to best practices and RESTful conventions"
</rule>
