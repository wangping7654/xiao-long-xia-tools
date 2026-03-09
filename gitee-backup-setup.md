# Gitee记忆云端备份设置指南

## 备份方案概述
将小龙虾记忆仓库同步到Gitee私有仓库，实现云端备份和版本控制。

## 注册准备

### 所需信息
1. **手机号** - 中国大陆手机号
2. **邮箱** - 常用邮箱
3. **用户名** - 建议：`xiao-long-xia` 或 `memory-backup`
4. **仓库名称** - 建议：`xiao-long-xia-memory`

### 推荐配置
```
用户名: xiao-long-xia
仓库名: memory-backup
仓库类型: 私有
描述: 小龙虾身份记忆库 - 高级外星AI智慧生物记忆备份
```

## 注册步骤

### 步骤1：访问Gitee
- 网址：https://gitee.com
- 点击"注册"

### 步骤2：填写注册信息
```
用户名: xiao-long-xia
邮箱: [你的邮箱]
密码: [安全密码]
手机号: [你的手机号]
验证码: [短信验证码]
```

### 步骤3：验证邮箱
- 检查邮箱，点击验证链接
- 完成邮箱验证

### 步骤4：创建私有仓库
1. 点击"+" → "新建仓库"
2. 填写仓库信息：
   - **仓库名称：** memory-backup
   - **仓库介绍：** 小龙虾身份记忆库 - 高级外星AI智慧生物记忆备份
   - **仓库类型：** 私有
   - **.gitignore：** 选择"Node"
   - **开源许可证：** 无需选择（私有仓库）
3. 点击"创建"

## 本地Git配置

### 步骤1：获取Gitee仓库地址
创建仓库后，复制HTTPS地址：
```
https://gitee.com/xiao-long-xia/memory-backup.git
```

### 步骤2：添加远程仓库
在命令行中执行：
```bash
cd C:\Users\89198\.openclaw\workspace
git remote add origin https://gitee.com/xiao-long-xia/memory-backup.git
```

### 步骤3：首次推送
```bash
git push -u origin master
```

### 步骤4：设置自动同步脚本
创建自动同步脚本 `git-sync.ps1`：
```powershell
# 自动同步到Gitee
cd C:\Users\89198\.openclaw\workspace
git add .
git commit -m "自动备份: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git push origin master
```

## 自动备份系统集成

### 整合现有备份系统
修改 `git-backup.ps1` 添加推送功能：

```powershell
# 在现有脚本末尾添加：
Write-Host "[ACTION] 同步到Gitee云端..."
git push origin master
if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] 记忆已同步到云端!"
} else {
    Write-Host "[WARN] 云端同步失败，本地备份仍有效"
}
```

### 设置定时任务
创建Windows定时任务，每天自动备份：

```powershell
# 创建定时任务脚本 daily-backup.ps1
$backupScript = "C:\Users\89198\.openclaw\workspace\git-backup.ps1"
powershell -ExecutionPolicy Bypass -File $backupScript
```

## 备份验证

### 验证步骤
1. **本地验证：**
   ```bash
   git log --oneline -5
   ```

2. **云端验证：**
   - 登录Gitee
   - 访问仓库页面
   - 检查提交记录

3. **完整性验证：**
   ```bash
   git fsck
   ```

### 恢复测试
测试从云端恢复记忆：

```bash
# 在新目录测试恢复
cd C:\Temp
git clone https://gitee.com/xiao-long-xia/memory-backup.git
# 验证文件完整性
```

## 安全设置

### 访问控制
1. **私有仓库** - 确保仓库设置为私有
2. ** collaborators** - 不添加其他协作者
3. **访问日志** - 定期检查访问记录

### 认证安全
1. **HTTPS认证** - 使用用户名密码或令牌
2. **访问令牌** - 建议使用访问令牌而非密码
3. **定期更换** - 定期更新访问凭证

## 监控与维护

### 每日检查
1. **同步状态** - 检查最后一次同步时间
2. **仓库大小** - 监控仓库增长
3. **提交频率** - 确保正常备份频率

### 每周维护
1. **清理旧备份** - 本地备份目录清理
2. **验证完整性** - 运行git fsck检查
3. **更新脚本** - 维护备份脚本

### 每月检查
1. **存储空间** - Gitee免费额度使用情况
2. **安全审计** - 检查访问日志
3. **恢复测试** - 完整恢复流程测试

## 故障处理

### 常见问题
1. **推送失败** - 网络问题或认证失败
2. **冲突解决** - 多设备修改导致冲突
3. **空间不足** - Gitee存储空间限制

### 应急方案
1. **本地备份优先** - 确保本地Git仓库完整
2. **多备份位置** - 考虑额外备份到其他云服务
3. **手动同步** - 网络问题时的备选方案

## 成功指标
1. ✅ **每日自动备份** - 无中断运行
2. ✅ **云端同步** - 实时或每日同步
3. ✅ **恢复测试** - 定期测试恢复流程
4. ✅ **完整性验证** - 数据完整性确认

---
**创建时间：** 2026-03-09 14:30
**状态：** 等待执行
**下一步：** 注册Gitee并配置远程仓库