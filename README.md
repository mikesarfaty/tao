# TAO (Terraform As Objects)

This library is a terraform object mapping. It currently does very little, but still **should** be able to parse the entire Terraform language into Python objects.

## Background

I am an SRE at @Twilio Segment; I was sick of seeing non-uniform Terraform usage. My day becomes a few seconds faster when files are named correctly, or when I can do large sweeping Terraform changes in regex. Unfortunately, regex is tough to use when trying to act on the logic in modules. For example, if I only want to update the ref for a module that uses a specific argument, imagine writing the regex for that. The goal of TAO is to be able to do wide, logical Terraform changes in as few lines as possible. 

Another thing I wish we could import into our existing pipelines is uniform module usage. If I have a module with inputs a, b, c, d, I would **love** if (a) I could run a command that will reorganize the modules to arrange their arguments in the "uniform" fashion, and (b) incorporate a CI check to fail any build that don't adhere to Terraform standards.

## What would I use this for?

When tao is finished, it will do any of the following in under 20 lines of code:
- batch update refs for modules
- enforce/update ordering of Arguments within modules or other blocks (ie, count must come first, then source, etc.)
- check abritrarily written styling rules (ie variables in variables.tf, outputs in outputs.tf)
- reorganize workspaces according to style rules (ie move all outputs to outputs.tf, module_x moved to module_x.tf)

Anything that you used to try and write complicated regex for, tao will be able to do.

## Roadmap
- [x] Initial object mapping (Blocks, Comments, Empty Lines, Arguments)
- [ ] Large scale testing + re-rendering to confirm parsing capabilities
- [ ] Tune the ordering of block contents (introduce weight property vs using order in contents list)
- [ ] Set up high-level API (stores, load+save)
- [ ] Finish certain Magic functions (eq, ...)
- [ ] Set up inheritence for reserved top-level blocks (data, resource, locals, terraform, module, provider)
- [ ] Set up inheritence for reserved Arguments (count, source, for_each)
- [ ] Set up dynamic blocks
- [ ] Render/tokenize ArgumentValues (currently strings)
