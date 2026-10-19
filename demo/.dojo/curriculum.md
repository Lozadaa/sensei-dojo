# Curriculum · Git

Base: an empty practice repo, `practice-git/`, created in kata 01 with `git init`, and
a practice remote on your GitHub or GitLab account from orange belt on. Every task and
question assumes Git 2.30 or later in the terminal.

Two forms: terminal / the editor's source control panel.

## Diagnóstico

1. White: which command shows what changed and what is staged? → `git status`
2. Yellow: which command creates a branch and switches to it in one step? → `git switch -c <branch>` (or `git checkout -b`)
3. Orange: which command downloads remote commits without merging them? → `git fetch`
4. Green: which command squashes the last three commits into one? → `git rebase -i HEAD~3` (squash)
5. Blue: which command finds the commit that broke something by halving the history? → `git bisect`

## Cinturón blanco · The repo and the first commit

### G-W1 Inside your repo            prereq: —
Why: knowing where history lives is what takes away the fear of deleting.
Kata (≤7 steps): create `practice-git/`, `git init`, look at the hidden `.git` folder, `git status`.
Diagram: where-in-the-tool: your folder, `.git/` inside it, history inside `.git/`.
Side by side: terminal / source control panel.
Questions (Q → expected A):
  - Which folder does git init create? → `.git`
  - If you delete `.git`, what do you lose? → the whole history (your files stay)
  - Which branch does git status say you are on? → `main` (with init.defaultBranch=main)
Traps: thinking the history lives "in the cloud".

### G-W2 Your first commit            prereq: G-W1
Why: without commits there is no history to recover or share.
Kata (≤7 steps): create notes.txt, git status, git add notes.txt, git status, git commit -m "first note", git log --oneline.
Diagram: flow working tree → staging → commit, staging highlighted.
Side by side: terminal / source control panel, same labels.
Questions (Q → expected A):
  - Which command stages notes.txt? → `git add notes.txt`
  - What heading does git status use for staged files? → `Changes to be committed`
  - After git add, is the file in the history? → no: it gets there with `git commit`
Traps: thinking add saves ("add picks, commit saves"); forgetting -m and landing in an editor.

### G-W3 Reading the history            prereq: G-W2
Why: before undoing anything you need to find where to go back to.
Kata (≤7 steps): three commits, git log, git log --oneline, git show HEAD~1.
Diagram: commits in a row with HEAD on the last one.
Side by side: git log / the editor's history view.
Questions (Q → expected A):
  - Which option shows one commit per line? → `--oneline`
  - Which key closes git log? → `q`
  - How do you name the commit before HEAD? → `HEAD~1` (or `HEAD^`)
Traps: pressing Esc or Ctrl+C to leave the pager.

### G-W4 .gitignore            prereq: G-W2
Why: generated files and secrets must never reach the history.
Kata (≤7 steps): create `build/` and `.env`, write .gitignore, git status before and after.
Diagram: before / after git status with the .gitignore.
Side by side: does not apply.
Questions (Q → expected A):
  - Which line ignores the whole build folder? → `build/`
  - Does .gitignore stop tracking a file that is already committed? → no: you need `git rm --cached`
  - Which command tells you which rule ignores a file? → `git check-ignore -v <file>`
Traps: thinking .gitignore deletes files.

## Cinturón amarillo · Undo and branch

### G-Y1 Undo without fear            prereq: G-W3
Why: undoing well is what lets you try things without fear.
Kata (≤7 steps): change notes.txt, git add, git restore --staged, git restore, a bad commit and git revert.
Diagram: three boxes (working tree, staging, commit) with the command that undoes each.
Side by side: terminal / panel buttons (Unstage, Discard, Revert).
Questions (Q → expected A):
  - Which command unstages a file without losing the change? → `git restore --staged <file>`
  - Which command discards a change that is not staged yet? → `git restore <file>`
  - Which command undoes an already shared commit by adding another? → `git revert <commit>`
Traps: `git reset --hard` as the answer to everything.

### G-Y2 Branches            prereq: G-W3
### G-Y3 Merging            prereq: G-Y2
### G-Y4 Resolving conflicts            prereq: G-Y3
### G-Y5 Detached HEAD            prereq: G-Y2

## Cinturón naranja · Working with a remote

### G-O1 Remotes: clone, fetch, pull, push            prereq: G-Y3
### G-O2 Remote branches and tracking            prereq: G-O1
### G-O3 Pull requests            prereq: G-O2, G-Y4
### G-O4 Rebase            prereq: G-Y5, G-O2
### G-O5 Stash            prereq: G-Y1

## Cinturón verde · Clean history

### G-G1 Interactive rebase and squash            prereq: G-O4
### G-G2 Cherry-pick            prereq: G-Y3
### G-G3 Tags and releases            prereq: G-O1

## Cinturón azul · Investigating

### G-B1 Blame and log -S            prereq: G-W3
### G-B2 Bisect            prereq: G-B1
### G-B3 Reflog: getting lost work back            prereq: G-Y5

## Cinturón marrón · Scale

### G-R1 Hooks            prereq: G-W2
### G-R2 Submodules            prereq: G-O1
### G-R3 Team workflows            prereq: G-O3

## Cinturón negro · Under the hood

### G-K1 Objects: blob, tree, commit            prereq: G-B3
### G-K2 Packfiles and performance            prereq: G-K1
### G-K3 Rewriting history at scale            prereq: G-G1, G-K1
