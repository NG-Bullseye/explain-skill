# explain

A skill for Claude Code and other agents that read `SKILL.md`. It makes the
agent explain a mechanism to a developer as a causal chain: the problem in the
first sentence, every claim with its because, in the words the developer
already uses, without analogies.

## The problem it solves

An agent asked "why is this a problem?" tends to answer with the effect and
leave out the cause, or to fall back on an analogy. Both fail for a developer
who knows the terms and is missing one link.

Asked why fail2ban does not protect an SSH port behind a Cloudflare tunnel,
the agent first wrote:

> All SSH connections arrive from 127.0.0.1, so IP-based tools do not help.
> Think of two doors: one with a key, one with a password ...

What the developer needed, in his own words:

> The problem is the second SSH path by password. With the username and
> password of the Mac anyone can connect by brute force. fail2ban does not
> protect, because it blocks by IP and through the tunnel everyone has the
> same incoming IP, since Cloudflare proxies.

Three sentences, each claim with its because, the chain ending at something
he already knew.

Existing skills cover parts of this. Answer-first and BLUF skills put the
answer in the first sentence. Feynman and ELI5 skills explain through
analogies and simplified language. None requires a reason on every claim,
none rules analogies out, none reads how the user talks about the topic.

## What the skill does

1. Collects the user's words. `user_words.py` reads earlier Claude Code
   session histories under `~/.claude/projects` and prints the messages the
   user typed about the topic. The agent sorts every term it needs into the
   user's term, or new word.
2. Writes the chain. Problem first, every claim with its because in the same
   sentence, the chain ending at known ground, three to five short sentences
   of running text that survive text-to-speech. New words get keywords in
   brackets once.
3. Names the corrections. Wording the code does not carry and wrong
   assumptions in the question are stated after the chain, one line each:
   you say / correct is / because.

The rules are in [`skills/explain/SKILL.md`](skills/explain/SKILL.md).

## Install

```
npx skills@latest add NG-Bullseye/explain-skill
```

or by hand:

```
git clone https://github.com/NG-Bullseye/explain-skill
ln -s "$PWD/explain-skill/skills/explain" ~/.claude/skills/explain
```

The agent loads it when the user asks why or how something works or fails,
says an explanation did not land, or wants an architecture made
understandable. `/explain` invokes it by hand.

## What is in it

Two files: `SKILL.md` and `user_words.py`. The script needs Python 3 and
nothing else. It only reads the local session histories, keeps messages the
user typed himself, drops pasted material, and prints to stdout. No network
access, no hooks, nothing that runs on its own.

```
python3 user_words.py tunnel ssh runner          # current project
python3 user_words.py --all-projects fail2ban    # every project
```

The examples in `SKILL.md` are German, the language of the first user. The
agent explains in whatever language the user writes.

## License

MIT
