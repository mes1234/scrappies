# Agent rules

## Abstract classes are read-only

- Do not edit, rename, move, or delete any abstract class or its members, in any file. An abstract class is one that inherits from `ABC` or uses `abc.abstractmethod`, or an equivalent in other languages (abstract classes, interfaces, protocols, traits).
- Before changing a file, check whether the code you would touch is part of an abstract class. If it is, leave it unchanged.
- If a task seems to need a change to an abstract class, stop and ask the user first. Propose the change instead of making it.
- Add new behavior in concrete subclasses or implementations instead.
