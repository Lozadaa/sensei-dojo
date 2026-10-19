# Curriculum · Git

Base: un repo de práctica vacío, `practica-git/`, creado en la kata 01 con `git init`, y
un remoto de práctica en tu cuenta de GitHub o GitLab desde el cinturón naranja. Todas
las tareas y preguntas asumen Git 2.30 o posterior en la terminal.

Formas del dominio: terminal / panel de control de código del editor.

## Diagnóstico

1. Blanco: ¿qué comando muestra qué archivos cambiaron y cuáles están en staging? → `git status`
2. Amarillo: ¿qué comando crea una rama y cambia a ella en un paso? → `git switch -c <rama>` (o `git checkout -b`)
3. Naranja: ¿qué comando trae los commits del remoto sin fusionarlos? → `git fetch`
4. Verde: ¿qué comando junta los tres últimos commits en uno? → `git rebase -i HEAD~3` (squash)
5. Azul: ¿qué comando busca el commit que rompió algo partiendo el historial en dos? → `git bisect`

## Cinturón blanco · El repo y el primer commit

### G-W1 El repo por dentro            prereq: —
Por qué: saber dónde vive el historial es lo que quita el miedo a borrar.
Kata (≤7 pasos): crea `practica-git/`, `git init`, mira la carpeta oculta `.git`, `git status`.
Diagrama: dónde-en-la-herramienta: tu carpeta, `.git/` dentro, el historial en `.git/`.
Lado a lado: terminal / panel de control de código.
Preguntas (Q → R esperada):
  - ¿Qué carpeta crea git init? → `.git`
  - Si borras `.git`, ¿qué pierdes? → todo el historial (tus archivos se quedan)
  - ¿Qué rama crea git init por defecto en Git 2.28+ con init.defaultBranch=main? → `main`
Trampas: creer que el historial está "en la nube".

### G-W2 Tu primer commit            prereq: G-W1
Por qué: sin commits no hay historial que recuperar ni compartir.
Kata (≤7 pasos): crea notas.txt, git status, git add notas.txt, git status, git commit -m "primera nota", git log --oneline.
Diagrama: flujo working tree → staging → commit, con staging en acento.
Lado a lado: terminal / panel de control de código, mismas etiquetas.
Preguntas (Q → R esperada):
  - ¿Qué comando pasa notas.txt a staging? → `git add notas.txt`
  - ¿Qué título usa git status para lo que está en staging? → `Changes to be committed`
  - ¿Un archivo tras git add ya está en el historial? → no: entra con `git commit`
Trampas: creer que add guarda ("add elige, commit guarda"); olvidar -m y quedar en el editor.

### G-W3 Leer el historial            prereq: G-W2
Por qué: antes de deshacer nada hay que encontrar a dónde volver.
Kata (≤7 pasos): tres commits, git log, git log --oneline, git show HEAD~1.
Diagrama: los commits en fila con HEAD apuntando al último.
Lado a lado: git log / vista de historial del editor.
Preguntas (Q → R esperada):
  - ¿Qué opción muestra un commit por línea? → `--oneline`
  - ¿Qué tecla cierra git log? → `q`
  - ¿Cómo nombras el commit anterior a HEAD? → `HEAD~1` (o `HEAD^`)
Trampas: pulsar Esc o Ctrl+C para salir del paginador.

### G-W4 .gitignore            prereq: G-W2
Por qué: lo generado y lo secreto no deben entrar nunca en el historial.
Kata (≤7 pasos): crea `build/` y `.env`, escribe .gitignore, git status antes y después.
Diagrama: antes / después de git status con el .gitignore.
Lado a lado: no aplica.
Preguntas (Q → R esperada):
  - ¿Qué línea ignora toda la carpeta build? → `build/`
  - ¿.gitignore deja de seguir un archivo que ya está en un commit? → no: hace falta `git rm --cached`
  - ¿Qué comando dice qué regla ignora un archivo? → `git check-ignore -v <archivo>`
Trampas: creer que .gitignore borra archivos.

## Cinturón amarillo · Deshacer y ramificar

### G-Y1 Deshacer sin miedo            prereq: G-W3
Por qué: deshacer bien es lo que permite probar cosas sin miedo.
Kata (≤7 pasos): un cambio en notas.txt, git add, git restore --staged, git restore, un commit malo y git revert.
Diagrama: tres cajas (working tree, staging, commit) con el comando que deshace cada una.
Lado a lado: terminal / botones del panel (Unstage, Discard, Revert).
Preguntas (Q → R esperada):
  - ¿Qué comando saca un archivo de staging sin perder el cambio? → `git restore --staged <archivo>`
  - ¿Qué comando descarta un cambio que aún no está en staging? → `git restore <archivo>`
  - ¿Qué comando deshace un commit ya compartido creando otro? → `git revert <commit>`
Trampas: `git reset --hard` como respuesta a todo.

### G-Y2 Ramas            prereq: G-W3
### G-Y3 Fusionar (merge)            prereq: G-Y2
### G-Y4 Conflictos a mano            prereq: G-Y3
### G-Y5 HEAD y detached HEAD            prereq: G-Y2

## Cinturón naranja · Trabajar con un remoto

### G-O1 Remotos: clone, fetch, pull, push            prereq: G-Y3
### G-O2 Ramas remotas y seguimiento            prereq: G-O1
### G-O3 Pull requests            prereq: G-O2, G-Y4
### G-O4 Rebase            prereq: G-Y5, G-O2
### G-O5 Stash            prereq: G-Y1

## Cinturón verde · Historial limpio

### G-G1 Rebase interactivo y squash            prereq: G-O4
### G-G2 Cherry-pick            prereq: G-Y3
### G-G3 Tags y versiones            prereq: G-O1

## Cinturón azul · Investigar

### G-B1 Blame y log -S            prereq: G-W3
### G-B2 Bisect            prereq: G-B1
### G-B3 Reflog: recuperar lo perdido            prereq: G-Y5

## Cinturón marrón · Escala

### G-R1 Hooks            prereq: G-W2
### G-R2 Submódulos            prereq: G-O1
### G-R3 Flujos de equipo            prereq: G-O3

## Cinturón negro · Por dentro

### G-K1 Objetos: blob, tree y commit            prereq: G-B3
### G-K2 Packfiles y rendimiento            prereq: G-K1
### G-K3 Reescribir historia a escala            prereq: G-G1, G-K1
