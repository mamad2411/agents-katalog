{
  description = "Nix for macOS configuration";

  # modules/base/nix.nix 直接复用此 attrset，避免两处列表漂移。
  nixConfig = {
    substituters = [
      "https://mirrors.ustc.edu.cn/nix-channels/store"
      "https://mirror.tuna.tsinghua.edu.cn/nix-channels/store"
      "https://nix-community.cachix.org"
      "https://cache.nixos.org"
    ];
    trusted-public-keys = [
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
    ];
  };

  inputs = {
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";

    nix-homebrew.url = "github:zhaofengli-wip/nix-homebrew";
    nix-darwin = {
      url = "github:lnl7/nix-darwin";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    homebrew-bundle = {
      url = "github:homebrew/homebrew-bundle";
      flake = false;
    };
    homebrew-core = {
      url = "github:homebrew/homebrew-core";
      flake = false;
    };
    homebrew-cask = {
      url = "github:homebrew/homebrew-cask";
      flake = false;
    };
    homebrew-services = {
      url = "github:homebrew/homebrew-services";
      flake = false;
    };
    aerospace = {
      url = "github:nikitabobko/homebrew-tap";
      flake = false;
    };
    daipeihust = {
      url = "github:daipeihust/homebrew-tap";
      flake = false;
    };
    stablyai-orca = {
      url = "github:stablyai/homebrew-orca";
      flake = false;
    };
    zen-browser = {
      url = "github:youwen5/zen-browser-flake";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    noctalia = {
      url = "github:noctalia-dev/noctalia";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    hibiki = {
      url = "github:linuxmobile/hibiki";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    plasma-manager = {
      url = "github:nix-community/plasma-manager";
      inputs.nixpkgs.follows = "home-manager";
      inputs.home-manager.follows = "home-manager";
    };
    catppuccin.url = "github:catppuccin/nix";
    agenix = {
      url = "github:ryantm/agenix";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
    orca = {
      url = "github:stslex/orca-nix";
      inputs.nixpkgs.follows = "nixpkgs-unstable";
    };
  };

  # The `outputs` function will return all the build results of the flake.
  # A flake can have many use cases and different types of outputs,
  # parameters in `outputs` are defined in `inputs` and can be referenced by their names.
  # However, `self` is an exception, this special parameter points to the `outputs` itself (self-reference)
  # The `@` syntax here is used to alias the attribute set of the inputs's parameter, making it convenient to use inside the function.
  outputs =
    inputs@{
      self,
      nixpkgs,
      nix-darwin,
      home-manager,
      nix-homebrew,
      agenix,
      git-hooks,
      ...
    }:
    let
      inherit (inputs.nixpkgs) lib;
      mylib = import ./lib { inherit lib; };
      myvars = import ./vars;

      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems =
        f:
        builtins.listToAttrs (
          map (system: {
            name = system;
            value = f system;
          }) systems
        );
      preCommit = import ./git-hooks.nix { inherit self git-hooks; };
      # currentSystem 在纯求值中不可用；原生系统 derivation 只在 --impure
      # 检查中暴露，跨平台的 pre-commit checks 仍可纯求值。
      evaluatorSystem = builtins.currentSystem or null;

      # 仓库约定默认位于 $HOME/nix-config；可用 NIX_CONFIG_ROOT 覆盖。
      # 纯求值时环境变量不可见，回退路径只用于判断 gitignored hosts/local/。
      configuredRoot = builtins.getEnv "NIX_CONFIG_ROOT";
      evaluationHome = builtins.getEnv "HOME";
      repositoryRoot =
        if configuredRoot != "" then
          configuredRoot
        else if evaluationHome != "" then
          "${evaluationHome}/${myvars.repositoryDirectory}"
        else
          "/home/${myvars.username}/${myvars.repositoryDirectory}";

      # specialArgs 内的参数可以在各个模块中访问到，只需要你添加到函数输入变量中即可
      specialArgs = {
        inherit
          inputs
          myvars
          mylib
          repositoryRoot
          ;
      };
      desktopProfile = {
        graphical = true;
        systemManaged = true;
      };
      headlessProfile = {
        graphical = false;
        systemManaged = false;
      };

      # 生成无 root 权限、无图形桌面的 standalone home-manager 配置
      mkHeadlessHome =
        system:
        home-manager.lib.homeManagerConfiguration {
          pkgs = import inputs.nixpkgs-unstable {
            inherit system;
            config.allowUnfree = true;
          };
          extraSpecialArgs = specialArgs // {
            hostProfile = headlessProfile;
          };
          modules = [
            ./home/remote-server.nix
            agenix.homeManagerModules.default
          ];
        };

      # 本机特定配置目录（gitignored，需要 --impure 构建）
      # 新机器部署：cp -r hosts/local.example hosts/local && 编辑其中的文件。
      localHostDir = "${repositoryRoot}/hosts/local";
      localHostModules = if builtins.pathExists localHostDir then mylib.scanPaths localHostDir else [ ];

      mkNixosSystem = nixpkgs.lib.nixosSystem {
        specialArgs = specialArgs // {
          hostProfile = desktopProfile;
        };
        system = "x86_64-linux";
        pkgs = import inputs.nixpkgs-unstable {
          system = "x86_64-linux";
          overlays = import ./overlays inputs;
          config.allowUnfree = true;
        };
        modules = [
          ./modules/base
          ./modules/linux
          ./modules/optional/desktop
          ./modules/optional/dev/python-dev.nix
          agenix.nixosModules.default

          home-manager.nixosModules.home-manager
          {
            home-manager = {
              useGlobalPkgs = true;
              useUserPackages = true;
              extraSpecialArgs = specialArgs // {
                hostProfile = desktopProfile;
              };
              backupFileExtension = "home-manager.backup";
              users.${myvars.username} = import ./home/nixos.nix;
            };
          }
        ]
        # 导入 hosts/local/ 中所有 .nix 文件（硬件配置、主机名等）
        ++ localHostModules;
      };

      mkDarwinSystem = nix-darwin.lib.darwinSystem {
        specialArgs = specialArgs // {
          hostProfile = desktopProfile;
        };
        system = "aarch64-darwin";
        pkgs = import inputs.nixpkgs-unstable {
          system = "aarch64-darwin";
          config.allowUnfree = true;
        };
        modules = [
          ./modules/base
          ./modules/macos
          ./modules/optional/dev/python-dev.nix
          agenix.darwinModules.default
          home-manager.darwinModules.home-manager
          {
            home-manager = {
              useGlobalPkgs = true;
              useUserPackages = true;
              extraSpecialArgs = specialArgs // {
                hostProfile = desktopProfile;
              };
              backupFileExtension = "home-manager.backup";
              users.${myvars.username} = import ./home/mac.nix;
            };
          }

          nix-homebrew.darwinModules.nix-homebrew
          {
            nix-homebrew = {
              enable = true;
              user = myvars.username;
              enableRosetta = true;
              autoMigrate = true;
              taps = {
                "homebrew/homebrew-bundle" = inputs.homebrew-bundle;
                "homebrew/homebrew-cask" = inputs.homebrew-cask;
                "homebrew/homebrew-core" = inputs.homebrew-core;
                "homebrew/homebrew-services" = inputs.homebrew-services;
                "nikitabobko/homebrew-tap" = inputs.aerospace;
                "daipeihust/homebrew-tap" = inputs.daipeihust;
                "stablyai/homebrew-orca" = inputs.stablyai-orca;
              };
              mutableTaps = false;
            };
          }
        ];
      };
    in
    {
      # 不只枚举 outputs：checks 直接引用各平台完整系统/activation derivation。
      checks = forAllSystems (
        system:
        {
          pre-commit-check = preCommit system;
        }
        // lib.optionalAttrs (evaluatorSystem == system && lib.hasSuffix "-linux" system) {
          headless-activation = (mkHeadlessHome system).activationPackage;
        }
        # NixOS modules contain Linux-only IFDs; expose this check only on Linux
        # hosts/CI so macOS --all-systems never tries to realise them.
        // lib.optionalAttrs (system == "x86_64-linux" && evaluatorSystem == "x86_64-linux") {
          nixos-system = mkNixosSystem.config.system.build.toplevel;
        }
        // lib.optionalAttrs (system == "aarch64-darwin" && evaluatorSystem == system) {
          darwin-system = mkDarwinSystem.system;
        }
      );

      # 开发 shell：进入后自动安装 git pre-commit hooks
      devShells = forAllSystems (system: {
        default = inputs.nixpkgs-unstable.legacyPackages.${system}.mkShell {
          inherit ((preCommit system)) shellHook;
        };
      });

      # macOS 配置
      darwinConfigurations."${myvars.macosHostname}" = mkDarwinSystem;

      # NixOS 配置（仅当 hosts/local/ 存在时定义，否则 nix flake check 在非 Linux 机器上会失败）
      nixosConfigurations = if builtins.pathExists localHostDir then { nixos = mkNixosSystem; } else { };

      # 无 root 权限、无图形桌面的 standalone home-manager 配置。
      # remote 名称保留为兼容别名；新命令使用语义更准确的 headless。
      homeConfigurations = {
        "headless" = mkHeadlessHome "x86_64-linux";
        "headless-aarch64" = mkHeadlessHome "aarch64-linux";
        "remote" = mkHeadlessHome "x86_64-linux";
        "remote-aarch64" = mkHeadlessHome "aarch64-linux";
      };
    };
}
