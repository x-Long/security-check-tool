# 该条命令只需操作一次，获取远程 develop 最新代码
git remote add wb git@github.com:albertofwb/security-check-tool.git


# 每次都需要使用本命令获取远程最新代码
git fetch wb develop


# 切换到 develop 分支
git checkout wb/develop

# 基于 develop 分支继续接下来的开发
# 每完成4个功能为一个阶段，从 stage_1 开始命名
# 每验收通过一次自动加一
git checkout -b stage_1
