" Prerequisites
if &compatible || exists('g:loaded_intellij')
  finish
elseif v:version < 704
  echohl WarningMsg 
  echomsg 'IntelliJ unavailable: requires Vim 7.4+'
  echohl None
  finish
elseif !has('python')
  echohl WarningMsg 
  echomsg 'IntelliJ unavailable: requires Vim with python 2.x support'
  echohl None
  finish
endif

" Boilerplate
let s:save_cpoptions = &cpoptions
set cpoptions&vim

" Initialize python
python import idea_vim

" Completion 
function! idea#complete(findstart, base)
  return pyeval('
               \idea_vim.complete(int(vim.eval("a:findstart")), 
               \                  vim.eval("a:base"))
               \')
endfunction

" Autoactivation

function! idea#autoactivate()
   if !empty(finddir('.idea', './;~'))
       setlocal omnifunc=idea#complete
       nnoremap <buffer> <C-]> :python idea_vim.resolve()<CR>
   endif
endfunction

augroup intellijintegration
    autocmd!
    autocmd BufNewFile,BufReadPost * call idea#autoactivate()
augroup end

" Boilerplate
let g:loaded_intellij = 1
let &cpoptions = s:save_cpoptions
unlet s:save_cpoptions
