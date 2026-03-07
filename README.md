# proxiesus-updater

这个项目会每 3 小时自动抓取 `CharlesPikachu/freeproxy` 仓库中的 `proxies.json`，筛选出 `country_code = US` 且 `protocol = socks5` 的代理，并更新根目录下的 `proxiesus.json`。

## 功能

- GitHub Actions 每 3 小时自动运行一次
- 支持手动触发工作流
- 自动去重（按 `ip:port:protocol`）
- 自动提交并推送最新的 `proxiesus.json`

## 文件结构

- `scripts/update_proxies.py`：抓取和筛选脚本
- `.github/workflows/update-proxiesus.yml`：定时任务
- `proxiesus.json`：生成结果文件

## 使用方法

1. 新建一个 GitHub 仓库。
2. 把本项目文件上传到仓库根目录。
3. 推送到 GitHub。
4. 进入仓库的 **Actions** 页面，启用工作流。
5. 可以先手动运行一次 `Update US SOCKS5 proxies`，确认 `proxiesus.json` 成功生成。

## 本地运行

```bash
python scripts/update_proxies.py
```

运行后会在项目根目录生成或更新 `proxiesus.json`。

## 输出格式

`proxiesus.json` 的结构如下：

```json
{
  "source": "https://raw.githubusercontent.com/CharlesPikachu/freeproxy/master/proxies.json",
  "generated_at": "2026-03-08T00:00:00+00:00",
  "total": 0,
  "proxies": []
}
```

## 注意

上游 `proxies.json` 目前文档示例显示，代理对象包含 `protocol`、`ip`、`port`、`country_code` 等字段，因此本项目按这些字段进行过滤。若上游字段结构变化，需要同步调整脚本。 
