# Writing a Genex plugin

Read this when the person wants Genex to work with an engine or tool it has no plugin for
(`plugins_find` answered `write-plugin`) and they said yes to having one written.

A Genex plugin is a folder: `plugin.json` (the manifest: what the plugin adds), `backend.mjs` (a
Node module whose functions answer its tools) and the skill files it teaches agents with. It can
add tools, know a kind of project by its files, tell the lead what it finds at Genex's moments (a
run's start and end, a save point, a restore, a health check), capture pictures of the game, name the kinds
of worker a lead may start, and keep an engine's scratch out of the project's history.

## The rules

1. Write it in this project, in `genex-plugins/<id>/`, where `<id>` is the plugin's id: lowercase
   letters, digits and dashes, starting with a letter. Never write it into Genex's own data, the
   person's Library folder or another project.
2. You cannot load a plugin or turn one on, and nothing you write or say counts as the person doing
   it. No tool does it for you; don't look for one.
3. A plugin's backend runs with the person's access: Genex doesn't sandbox its code. Write only what
   its tools need. Don't start programs from it (Genex warns the person about any backend that
   does): talk to the engine, and leave its command-line programs to the lead, who runs them as
   jobs. Stay inside the project the call is bound to, open the network only to the hosts a tool
   needs, and keep no secret in a file.
4. Learn the engine's real command line and file layout from its own documentation or its `--help`
   before writing a tool; never guess a flag.

## The steps

1. Read the three references with `genex__skill`, passing their file:
   `skills/plugin-author/references/manifest.md` (every manifest section, and a complete
   `plugin.json` for a made-up engine, Sketch), `skills/plugin-author/references/backend.md` (its
   `backend.mjs`) and `skills/plugin-author/references/skill.md` (its own skill file).
2. Start from the Sketch example. Rename it, keep the sections the engine needs and drop the rest:
   only the identity fields and the `tools`, `skills`, `panels`, `settings` and `actions` lists are
   required, and the lists may be empty.
3. If you have `plugin_check`, check it with `plugin_check {"folder": "genex-plugins/<id>"}`. Fix
   every problem it names and check again until it answers `ok`. Read its scan findings: each one is
   something the person is told before they load it, so remove what the plugin doesn't need. Not
   every session has it (a Loop's lead or worker, or a local model, doesn't): without it, tell the
   person the plugin is ready and that the chat checks it before they load it.
4. Tell the person how to load it, in these words, and end your reply there:

   > Plugins → Add → Load local plugin…, choose genex-plugins/<id>. It starts off; turn it on there. It runs with your access; each of its tools asks before an agent runs it, and its own steps at Genex's moments don't ask.

Once the person has turned it on, its tools reach the projects its facts name. Genex keeps its own
copy of what was loaded: after a change, check the folder again as step 3 says and ask the person
to load it again the same way, in the words `plugin_check` gives when you have it. A plugin that is on stays
on when it is loaded again: its new code runs at once, and each of its tools asks again. Never
suggest Watch folder for it: Genex refuses to watch a folder agents write in, so each change is
loaded again by hand.
