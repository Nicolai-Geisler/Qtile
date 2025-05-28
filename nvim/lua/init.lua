require("config.lazy")

vim.cmd.colorscheme "catppuccin-latte"

vim.keymap.set('n', '<F4>', ':NvimTreeToggle<CR>', { noremap = true, silent = true })
