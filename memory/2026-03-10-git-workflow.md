# Git工作流程规范 - 2026-03-10

## 🎯 核心原则
**双保险备份策略**：本地git + 远程仓库（Gitee + GitHub）

## 📋 工作流程

### 1. 日常操作流程
```
开始工作 → 修改文件 → git备份 → 继续工作 → 每日结束前push
```

### 2. 具体步骤
#### A. 完成一部分工作后
1. **检查状态**：`git status`
2. **添加更改**：`git add .`
3. **提交备份**：`git commit -m "描述性消息"`
4. **本地备份完成**

#### B. 每天结束前
1. **推送到Gitee**：`git push origin master`
2. **推送到GitHub**：`git push github master`
3. **双远程备份完成**

### 3. 恢复流程（如果出错）
1. **查看提交历史**：`git log --oneline`
2. **恢复到指定版本**：`git reset --hard <commit-hash>`
3. **或使用标签恢复**：`git checkout <tag-name>`

## 🔧 当前配置
- **本地仓库**：`C:\Users\89198\.openclaw\workspace`
- **远程仓库1**：Gitee (`origin`) - https://gitee.com/little-dragon-shrimp/memory-backup.git
- **远程仓库2**：GitHub (`github`) - https://github.com/wangping7654/xiao-long-xia-tools.git

## 💡 最佳实践
1. **频繁提交**：每完成一个逻辑单元就提交
2. **描述性消息**：清楚说明做了什么更改
3. **每日推送**：确保远程备份最新
4. **忽略子模块**：`projects/paperclip`是子模块，主仓库不跟踪其内容更改

## 🚨 注意事项
- 子模块更改需要进入子模块目录单独提交
- 主仓库只跟踪子模块的引用，不跟踪具体内容
- 使用`git submodule update`更新子模块

## 📝 示例命令
```bash
# 日常备份
git status
git add .
git commit -m "完成XX功能/修复XX问题"

# 每日推送
git push origin master
git push github master

# 恢复操作
git log --oneline
git reset --hard abc1234
```

记住：**先git备份，再继续工作；每日结束前，双远程推送。**