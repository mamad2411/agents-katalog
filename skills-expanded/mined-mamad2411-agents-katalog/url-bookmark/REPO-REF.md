# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-next-open-ai-openclawx-url-bookmark/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 根据用户指令将 URL 保存为收藏，并匹配系统中已维护的标签。当用户说「收藏这个链接」「把这条存到技术标签」「保存网址」等时使用。先调用 get_bookmark_tags 获取可用标签列表；若缺少用户想要的标签，可用 add_bookmark_tag 新增标签，再根据用户意图选择标签，最后用 save_bookmark 保存。
