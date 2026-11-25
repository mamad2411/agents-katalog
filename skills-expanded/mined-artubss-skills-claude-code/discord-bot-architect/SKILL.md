---
name: discord-bot-architect
description: "Habilidade especializada para construir bots Discord prontos para produção. Abrange Discord.js (JavaScript) e Pycord (Python), gateway intents, slash commands, componentes interativos, rate limiting e sharding."
source: vibeship-spawner-skills (Apache 2.0)
---

# Arquiteto de Bot Discord

## Padrões

### Fundação Discord.js v14

Configuração moderna de bot Discord com Discord.js v14 e slash commands

**Quando usar**: ['Construir bots Discord com JavaScript/TypeScript', 'Precisa de conexão gateway completa com eventos', 'Construir bots com interações complexas']

```javascript
// src/index.js
const { Client, Collection, GatewayIntentBits, Events } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
require('dotenv').config();

// Crie o cliente com os intents mínimos necessários
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    // Adicione apenas o que você precisa:
    // GatewayIntentBits.GuildMessages,
    // GatewayIntentBits.MessageContent,  // PRIVILEGIADO - evite se possível
  ]
});

// Carregue comandos
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(f => f.endsWith('.js'));

for (const file of commandFiles) {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  if ('data' in command && 'execute' in command) {
    client.commands.set(command.data.name, command);
  }
}

// Carregue eventos
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(f => f.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args));
  } else {
    client.on(event.name, (...args) => event.execute(...args));
  }
}

client.login(process.env.DISCORD_TOKEN);
```

```javascript
// src/commands/ping.js
const { SlashCommandBuilder } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Replies with Pong!'),

  async execute(interaction) {
    const sent = await interaction.reply({
      content: 'Pinging...',
      fetchReply: true
    });

    const latency = sent.createdTimestamp - interaction.createdTimestamp;
    await interaction.editReply(`Pong! Latency: ${latency}ms`);
  }
};
```

```javascript
// src/events/interactionCreate.js
const { Events } = require('discord.js');

module.exports = {
  name: Events.InteractionCreate,
  async execute(interaction) {
    if (!interaction.isChatInputCommand()) return;

    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) {
      console.error(`No command matching ${interaction.commandName} was found.`);
      return;
    }

    try {
      await command.execute(interaction);
    } catch (error) {
      console.error(error);
      if (interaction.replied || interaction.deferred) {
        await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
      } else {
        await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
      }
    }
  }
};
```

### Fundação Pycord Bot

Bot Discord com Pycord (Python) e application commands

**Quando usar**: ['Construir bots Discord com Python', 'Preferir padrões async/await', 'Precisar de bom suporte a slash commands']

```python
# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Configure intents - ative apenas o que você precisa
intents = discord.Intents.default()
# intents.message_content = True  # PRIVILEGIADO - evite se possível
# intents.members = True          # PRIVILEGIADO

bot = commands.Bot(
    command_prefix="!",  # Legado, prefira slash commands
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Sincronize comandos (faça isto com cuidado - veja sharp edges)
    # await bot.sync_commands()

# Slash command
@bot.slash_command(name="ping", description="Check bot latency")
async def ping(ctx: discord.ApplicationContext):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Pong! Latency: {latency}ms")

# Slash command com opções
@bot.slash_command(name="greet", description="Greet a user")
async def greet(
    ctx: discord.ApplicationContext,
    user: discord.Option(discord.Member, "User to greet"),
    message: discord.Option(str, "Custom message", required=False)
):
    msg = message or "Hello!"
    await ctx.respond(f"{user.mention}, {msg}")

# Carregue cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.environ["DISCORD_TOKEN"])
```

```python
# cogs/general.py
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="info", description="Bot information")
    async def info(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Bot Info",
            description="A helpful Discord bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
```

### Padrão de Componentes Interativos

Uso de botões, menus de seleção e modals para UX rica

**Quando usar**: ['Precisa de interfaces de usuário interativas', 'Coletar entrada do usuário além de opções de slash command', 'Construir menus, confirmações ou formulários']

```javascript
// Discord.js - Botões e Select Menus
const {
  SlashCommandBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  StringSelectMenuBuilder,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle
} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('menu')
    .setDescription('Shows an interactive menu'),

  async execute(interaction) {
    // Linha de botões
    const buttonRow = new ActionRowBuilder()
      .addComponents(
        new ButtonBuilder()
          .setCustomId('confirm')
          .setLabel('Confirm')
          .setStyle(ButtonStyle.Primary),
        new ButtonBuilder()
          .setCustomId('cancel')
          .setLabel('Cancel')
          .setStyle(ButtonStyle.Danger),
        new ButtonBuilder()
          .setLabel('Documentation')
          .setURL('https://discord.js.org')
          .setStyle(ButtonStyle.Link)  // Link buttons don't emit events
      );

    // Linha de select menu (um por linha, ocupa todos os 5 slots)
    const selectRow = new ActionRowBuilder()
      .addComponents(
        new StringSelectMenuBuilder()
          .setCustomId('select-role')
          .setPlaceholder('Select a role')
          .setMinValues(1)
          .setMaxValues(3)
          .addOptions([
            { label: 'Developer', value: 'dev', emoji: '💻' },
            { label: 'Designer', value: 'design', emoji: '🎨' },
            { label: 'Community', value: 'community', emoji: '🎉' }
          ])
      );

    await interaction.reply({
      content: 'Choose an option:',
      components: [buttonRow, selectRow]
    });

    // Colete respostas
    const collector = interaction.channel.createMessageComponentCollector({
      filter: i => i.user.id === interaction.user.id,
      time: 60_000  // 60 segundos timeout
    });

    collector.on('collect', async i => {
      if (i.customId === 'confirm') {
        await i.update({ content: 'Confirmed!', components: [] });
        collector.stop();
      } else if (i.customId === 'cancel') {
        await i.update({ content: 'Cancelled!', components: [] });
        collector.stop();
      } else if (i.customId === 'select-role') {
        await i.update({ content: `You selected: ${i.values.join(', ')}`, components: [] });
        collector.stop();
      }
    });

    collector.on('end', collected => {
      console.log(`Collected ${collected.size} interactions`);
    });
  }
};
```

```python
# Pycord - Botões e Select Menus
import discord
from discord.ui import Button, View, Select

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.selected_value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.primary, custom_id="confirm")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.selected_value = "confirmed"
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, custom_id="cancel")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.selected_value = "cancelled"
        self.stop()

    @discord.ui.select(
        placeholder="Choose a role",
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="Developer", value="dev", emoji="💻"),
            discord.SelectOption(label="Designer", value="design", emoji="🎨"),
            discord.SelectOption(label="Community", value="community", emoji="🎉")
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.selected_value = select.values
        self.stop()

@bot.slash_command(name="menu", description="Shows an interactive menu")
async def menu(ctx: discord.ApplicationContext):
    view = MyView()
    await ctx.respond("Choose an option:", view=view)
    await view.wait()
    await ctx.followup.send(f"You selected: {view.selected_value}")
```

## Anti-Padrões

### ❌ Message Content para Comandos

**Por que é ruim**: Message Content Intent é privilegiado e descontinuado para comandos de bot.
Slash commands são a abordagem pretendida.

### ❌ Sincronizar Comandos a Cada Início

**Por que é ruim**: O registro de comandos tem rate limit. Comandos globais levam até 1 hora
para se propagar. Sincronizar a cada início desperdiça chamadas de API e pode atingir limites.

### ❌ Bloquear o Event Loop

**Por que é ruim**: O gateway Discord requer heartbeats regulares. Operações de bloqueio
causam heartbeats perdidos e desconexões.

## ⚠️ Arestas Perigosas

| Problema | Severidade | Solução |
|----------|-----------|--------|
| Slash command não responde a tempo | critical | Reconheça imediatamente, processe depois |
| Comandos globais não aparecem | critical | Etapa 1: Ative no Developer Portal |
| Rate limit de sincronização | high | Use um script de deploy separado (não na inicialização) |
| Token exposto em repositório | critical | Nunca hardcode tokens |
| Bot recusado ao se juntar ao servidor | high | Gere URL de convite correta |
| Sincronização lenta de comandos | medium | Desenvolvimento: Use comandos de guilda |
| Bot desconecta frequentemente | medium | Nunca bloqueie o event loop |
| Modal nunca aparece | medium | Mostre modal imediatamente |