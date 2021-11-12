# AtlassianAsst
自用小助手 For Atlassian。目前仅实现以下功能。
## Jira
对 Jira 的群组进行再次包装，以实现每个项目组可以管理对应群组的成员。
* 限制：实现指定用户，可管理多个 Jira 中的群组，可往用户管理的 Jira 群组中添加及移除用户。
* 限制：每个用户仅能查看自己创建的“用户与群组操作”操作，超级管理员能更改“用户与群组操作”中的“可查看人”来使其他人可查看。
* 开放 API，方便其他系统调用（钉钉，OA等）。API 未作以上的限制，使用 Jira 管理员直接操作群组中的用户。
## pip 依赖
pip install django==2.2.* django-simpleui atlassian-python-api
