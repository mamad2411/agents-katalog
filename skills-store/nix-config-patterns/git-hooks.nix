# Pre-commit hooks 配置 (git-hooks.nix)
#
# 用法：
#   nix flake check                    # 手动运行一次检查
#   nix develop                        # 进入 devShell，shellHook 自动安装 hooks
#   pre-commit run --all-files         # 手动对全部文件运行 hooks
{ self, git-hooks }:
system:
git-hooks.lib.${system}.run {
  src = self;
  hooks = {
    # Nix 格式化（RFC 风格，与 nixpkgs 一致）
    nixfmt.enable = true;
    # Nix 静态分析；现有警告已清理，后续提交不得回归。
    statix.enable = true;
    # 检测未使用的 Nix 绑定
    deadnix = {
      enable = true;
      # Nix 模块惯用写法：{ pkgs, myvars, ... } 中未用参数不算死代码
      settings.noLambdaPatternNames = true;
    };
    # 删除行尾空白
    trim-trailing-whitespace.enable = true;
    # 确保文件以换行结尾
    end-of-file-fixer.enable = true;
  };
}
