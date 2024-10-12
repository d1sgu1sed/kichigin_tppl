section .text
global _start

%macro pushd 0
    push rax
    push rbx
    push rcx
    push rdx
%endmacro

%macro popd 0
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

%macro print 2
    pushd
    mov rax, 1
    mov rdi, 1
    mov rsi, %1
    mov rdx, %2
    syscall
    popd
%endmacro

%macro dprint 0
    pushd
    mov rbx, 0
    mov rcx, 10
    %%divide:
        xor rdx, rdx
        div rcx
        push rdx
        inc rbx             
        cmp rax, 0
        jne %%divide
    %%digit:
        pop rax
        add rax, '0'
        mov [result], rax
        print result, 1
        dec rbx
        cmp rbx, 0
        jg %%digit
    popd
%endmacro

_start:
    mov rax, 0
    mov rbx, 0

    jmp check_lens

print_x:
    mov eax, [x + 4*rbx]
    dprint
    print space, slen
    inc rbx
    cmp rbx, x_len
    jne print_x

    mov rbx, 0
    print newline, nlen
    jmp print_y

print_y:
    mov eax, [y + 4*rbx]
    dprint
    print space, slen
    inc rbx
    cmp rbx, y_len
    jne print_y

    jmp check_lens

check_lens:
    mov eax, x_len
    mov ebx, y_len
    cmp eax, ebx
    jne end

    mov rax, 0
    mov rbx, 0
    jmp sum

sum:
    add eax, [x + 4*rbx]
    sub eax, [y + 4*rbx]
    inc rbx
    cmp rbx, x_len
    jne sum

    jmp print_minus

print_minus:
    cmp eax, 0
    jnl print_average
    print minus, mlen
    neg eax

print_average:
    mov rcx, x_len
    div rcx
    dprint
    cmp rdx, 0
    je print_done
    jmp print_point

print_point:
    print point, plen
    mov rbx, 0
    jmp print_frac

print_frac:
    mov rcx, 10
    mov rax, rdx
    mul rcx
    mov rcx, x_len
    div rcx
    dprint
    inc rbx
    cmp rdx, 0
    je print_done
    cmp rbx, 10
    jle print_frac

print_done:
    print newline, nlen
    jmp end

end:
    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    x dd 5, 3, 2, 6, 1, 7, 4
    x_len equ (($ - x)/4)
    y dd 0, 10, 1, 9, 2, 8, 5
    y_len equ (($ - y)/4)

    newline db 0xA, 0xD
    nlen equ $ - newline

    space db ' '
    slen equ $ - space

    minus db '-'
    mlen equ $ - minus

    point db '.'
    plen equ $ - point

section .bss
    result resb 1
