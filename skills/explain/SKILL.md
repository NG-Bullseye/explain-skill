---
name: explain
description: Explain as a causal chain in the user's own words - problem first, every claim with its because, in spoken technical prose. Use when the user asks why or how something works or fails, asks what the problem is, says an explanation did not land, or needs the architecture of a system or change made understandable.
---

An explanation here is a **causal chain** in the **user's words**: a few short sentences in which each claim carries its reason, built from the terms the user already works with, read in one pass, aloud if need be.

## 1. Collect the user's words

The explanation attaches to what the user knows, and what he knows shows in the words he types. Before explaining a topic for the first time in a session, read how he has talked about it:

```
python3 <this skill's folder>/user_words.py <keyword> [<keyword> ...]
python3 <this skill's folder>/user_words.py --all-projects <keyword> ...
```

It prints the messages the user typed in earlier Claude sessions that contain a keyword, newest first, for the current project or for all. Pick keywords from his question and from the topic (component names, tools, the thing that fails). Add his messages of the current conversation.

From these, note three things:

- **his terms**: the word he uses for each thing ("zweiter SSH-Weg", "incoming IP", "proxied"). Use exactly these, also where the code or the docs name it differently.
- **known ground**: what he has stated or used correctly. A chain may end there.
- **gaps**: terms from the topic he has never used. Each is a new word.

Done when every term the explanation needs is sorted into his term, or new word.

## 2. Write the chain

1. **Problem first.** The first sentence names the problem or the answer itself: "Das Problem ist X." When the user asked a direct question ("wozu das Passwort?"), the first sentence answers exactly that question.
2. **Every claim carries its because.** Attach the reason in the same sentence with weil / da / durch. An effect stated alone is an open link: "alle Verbindungen kommen von 127.0.0.1" explains nothing until "fail2ban sperrt nach IP" stands next to it.
3. **Chain to known ground.** Follow the becauses until the last one is known ground. Stop there.
4. **His terms, the mechanism itself.** State the actual mechanism literally, in his terms. Analogies, images and invented casts are out.
5. **New words in brackets.** A new word appears once with keywords in brackets right behind it, then bare: "HostKeyAlias (SSH-Option: prüft den Host-Key gegen einen anderen Eintrag in known_hosts)". Keywords, not a sentence.
6. **Spoken prose.** Three to five short declarative sentences, one link per sentence, in the order cause to effect. Plain running text that survives text-to-speech: no headings, tables or bullet lists inside the explanation.

For architecture the chain runs along the path of one request or one change: which part acts, what it hands to the next, why the next can or cannot do its job with that.

## 3. Name the corrections

The user's wording and assumptions are checked against the code and the facts, and every deviation is named - after the chain, one line each, as "du sagst … / richtig ist … , weil …":

- **wording that the code does not carry**: he says "Passkey", it is a keychain entry; he says "Runner fällt aus", the runner is a container and Docker fails. Give the name the code or tool uses, so his next question and his next search hit.
- **wrong assumption**: something he takes as given that is not so ("das Passwort brauche ich für die Verbindung"). Say what holds instead and its because.

Verify against the code or the system before correcting; a correction from memory is a guess. Keep using his term afterwards only where it was right.

## Model

A user's own wording of the explanation he should have been given (why fail2ban does not protect SSH behind a Cloudflare tunnel). The examples here are German; explain in the language the user writes in.

> Das Problem ist der zweite SSH-Weg per Passwort. Mit Username und Userpasswort des Macs kann jeder per Brute Force eine Verbindung herstellen. fail2ban schützt nicht, weil es IP-based Blocking ist und durch den Tunnel jeder dieselbe incoming IP hat, da Cloudflare proxied.

## Done when

Before sending, check each sentence:

- the first sentence names the problem or answers the question asked;
- every claim has its because in the same sentence;
- the last because is known ground for this user;
- every term is his term, or a new word with its bracket;
- every wrong wording and wrong assumption in his question is named with its correction.

When the user still does not follow, find the one link whose because is missing and supply that link alone, in one sentence. Concrete values (two IPs, one request) come in only there, to close that link.

What to do next (options, commands, a recommendation) follows after the explanation, separated from it, and only when asked for or needed to act.
