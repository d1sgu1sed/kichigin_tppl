section .data
    num dq 144
    result dq 0
    message db 'Result: ', 0
    buffer db '   ', 0 

section .bss
    x1 resq 1
    x2 resq 1

section .text
    global _start

_start:
    mov rax, [num]
    shr rax, 1
    mov [x1], rax

calculate:
    mov rax, [num]
    mov rbx, [x1]
    xor rdx, rdx
    div rbx
    add rax, [x1]
    shr rax, 1
    mov [x2], rax

    mov rax, [x1]
    sub rax, [x2]
    cmp rax, 1
    jge update_x1

    mov rax, [x2]
    mov [result], rax

    call to_string

    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, 8
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, buffer
    mov rdx, 10    
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

update_x1:
    mov rax, [x2]
    mov [x1], rax
    jmp calculate

to_string:
    mov rax, [result]
    mov rdi, 10
    mov rbx, buffer + 9 
    mov byte [rbx], 0

.convert_loop:
    xor rdx, rdx
    div rdi
    dec rbx
    add dl, '0'
    mov [rbx], dl
    test rax, rax
    jnz .convert_loop

    mov rsi, rbx
    ret
