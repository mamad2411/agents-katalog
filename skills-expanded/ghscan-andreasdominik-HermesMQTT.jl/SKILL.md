# How to write a new skill

Because of the fact that all HermesMQTT skills are executed within
the same Julia process, there is some more overhead in the code of the skills
compared to standalone Python skills.

To support skill development, the framework comes with a generator 
script, that creates a skill-skeleton that already is functional
without the need of wrinting any code manually.

This brief tutorials guides through the process of
making a new skill using the generator script:


## Set up the framework 

See section *Installation* for details. 
Let us assume, `HermesMQTT` is installed at `/opt/HermesMQTT/`.


## Define the intents

It is a good idea, to start skill development in the *Rhasspy*
console (aka web interface) and define the intents 
by adding slots and intents to the sentences file or (better)
add a new sentences file for each skill.

This way, it is possible to train the speech-to-text engine and 
test all wanted commands *and* to see all generated JSON payloads which
your new skill may need to read.


## Generate the skeleton a new project

To generate the skill, 
start a Julia REPL and run the skill-generator.
The genrator will ask you for the name of the skill, the names
of the intents and the names of the slots for each intent.

```julia
using HermesMQTT
HermesMQTT.generate_skill() # or HermesMQTT.generate_skill("SkillName")
```

The generator asks you to enter
+ the skill name (if not given as argument),
+ one by one the intent names for the skill,
+ for each intent, the needed slot names.

The generated skill is functional out of the box. When the
HermesMQTT-framework is restarted, it will load the new skill.
Because the intents are already defined in *Rhasspy*,
they can be tested instantly.

Of course, the actual implementation of the skill is missing, but
if called by the voice command, the new skill will prove that it is
alive by telling  you
it's name and names and values for all recognised slots.


## Add implementation

The actual implementation fo the skill can be added by modifying the 
action-functions for each intent.
These functions are located in the file
`Your_Skill/Skill/skill-actions.jl` and have the signatures
`<intentname>_action(topic, payload)`.

It is easy to change the dummy-implementation into whatever is needed.



### Files in the sceleton

Although all custom implementation can be done in the file `skill-actions.jl`, the created skeleton consists of several files. 
These may be modified, if wanted:


filename | comment | needs to be adapted
---------|---------|--------------------
`loader-MyFire.jl` | generated loader function for the framework | no
`config.ini`       | ini file as default                          | yes
`api.jl`           | source code of Julia low-level API for a controlled device | optional
`config.jl`   | global initialisation of a skill                 | optional
`exported.jl` | generated exported functions of the skill module  | no
`skill-actions.jl` | functions to be executed, if an intent is recognised | yes
`MyFire.jl`        | the julia module for the skill              | no

In a minimum-setup only 2 things need to be adapted for a new
skill:
- the action-functions which respond to an intent (the *direct* action, no callback)
  must be defined and implemented (in `skill-actions.jl`)
- settings and sentences to be utterd 
  in the `config.ini`-file


Optionally, more fine-grained software engineering is possible by
- separating the user-interaction from the API of controlled devices 
  (the latter might go to `api.jl`).
- and by using different intents, depending on the language
  defined in `config.ini`.


## Example with low-level API

This tutorial shows how a skill to control an external device
can be derived from the template.

The idea is to control an Amazon fire stick with a minimum set of commands
`on, off, play, pause`.
More commands can be implement easily the same way.

Switching on and off is implemented based on the common on-off-intent,
included in the framework.


### The Amazon fire low-level API

The low-level API which sends commands to the Amazon fire is borrowed from
Matt's ADBee project (`git@github.com:mattgyver83/adbee.git`) that provides
a shell-script to send commands to the Amazon device.
Please read there for the steps to prepare the Amazon device for
the remote control via ADB.

Although Python programmes usually find Python packages for every task, it is
a very good idea to implement the lowest level of any device-control API
as a shell script. Advantages:
- easy to write
- fast and without any overhead
- easy to test: the API can be tested by running the script
  from the commandline as `controlFire ON` or `controlFire OFF` and see
  what happens.

 The simplified ADBee-script is:

```sh
#!/bin/bash -xv
# control fireTv via adb

COMMANDS=$@
IP=amazon-fire  # set to 192.168.1.200 by dhcp
PORT=5555
ADB=adb
SEND_KEY="$ADB -s $IP:$PORT shell input keyevent"

adb connect amazon-fire

for CMD in $COMMANDS ; do
  case $CMD in
    wake)
      $SEND_KEY KEYCODE_WAKEUP
      ;;
    sleep)
      $SEND_KEY KEYCODE_POWER
      ;;
    play)
      $SEND_KEY KEYCODE_MEDIA_PLAY_PAUSE
      ;;
    pause)
      $SEND_KEY KEYCODE_MEDIA_PLAY_PAUSE
      ;;
    # more commands may go here ...
  esac
done
```

Once this script is tested, the Julia API can be set up.


### The Julia API

By default the API goes into the file api.jl, which is empty
in the template.

In this case only a wrapper is needed, to make the API-commands
available in the Julia program.
The framework provide a function `tryrun()` to execute external
commands safely (i.e. if an error occures, the program will not crash,
but reading the error message via Hermes text-to-speech).

This API definition splits in the function to execute the ADBee-script and
functions to be called by the user:

```Julia
function adbCmds(cmds)

    return tryrun(`$ADB $(split(cmds))`, errorMsg =
            """An error occured while sending commands $cmds
            to Amazon fire."""
end




function amazonON()
    adbCmds("wake")
end

function amazonOFF()
    adbCmds("sleep")
end

function amazonPlay()
    adbCmds("play")
end

function amazonPause()
    adbCmds("pause")
end
```


### The skill-action for on/off

This functions are executed by the framework if an intent is
recognised.
The functions are defined in the file `skill-actions.jl`.
On/off is handled via the common on/off-intent. All other actions
need a specific intent, that must be set up in the Snips console.

The constants `DEVICE_NAME` and `SLOT_NAME`, used in the example, 
can be defined
somewhere (by default constants are defined in `config.jl`):

```Julia
"""
    power_on_off(topic, payload)

Power on or of with HermesMQTT mechanism.
"""
function power_on_off(topic, payload)

    if is_on_off_matched(payload, DEVICE_NAME) == :on
        publish_end_session("I wake up the Amazon Fire Stick.")
        amazonON()
        return true

    elseif is_on_off_matched(payload, DEVICE_NAME) == :off
        publish_end_session("I send the Amazon Fire Stick to sleep.")
        amazonOFF()
        return true

    else
        return false
    end
end
```

Returning `false` will disable the *continue without hotword* function; i.e.
a hotword is necessary before the next command can be uttered.
This is necessary for the default-case, because probably a different
app will execute this non-recognised command.


### The skill-action for all other commands

All other commands must be handled by an intent that you must
create in the Rhasspy console.
Let's assume the intent has the name `MyFire` and delivers
the command in the slot `Command`.
The slot should know all known commands with synonyms.

If the intend have not been already generated, a
 skill-action has to be defined in the file
`skill-actions.jl`:

```Julia
"""
    action_commands(topic, payload)

Send commands to Amamzon device.
"""
function action_commands(topic, payload)

    if is_in_slot(SLOT_NAME, "play")
        publish_end_session("I play the current selection!")
        amazonPlay()
        return true

    elseif is_in_slot(SLOT_NAME, "pause")
        publish_end_session("I pause the movie.")
        amazonPause()
        return true

    else
        publish_end_session("I cannot respond!")
        return true
    end
end
```


### Tying everything together

The last step is to tell the skill the names of intents to listen to
and the names of the slots to extract values from.
Both is defined in the file `config.jl`:

- The slot names are simply defined as global constants
  (they are only global within the module MyFire).
- Intents and respective functions are stored in the background
  and registered with the function `register_intent_action()`.
  (the generator script is doing this registration for you)

```Julia
const SLOT_NAME = "Command"
const DEVICE_NAME = "amazon_fire"

...

register_on_off_action(power_on_off)
register_intent_action("MyFire", action_commands)
```

Once the functuions are registered together with the intents,
the framework will execute the functions.
