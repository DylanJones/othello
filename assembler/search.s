	.file	"search.c"
	.text
	.globl	_Z11countColorsPhc
	.type	_Z11countColorsPhc, @function
_Z11countColorsPhc:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -24(%rbp)
	movl	%esi, %eax
	movb	%al, -28(%rbp)
	movl	$0, -8(%rbp)
	movl	$0, -4(%rbp)
.L7:
	cmpl	$63, -4(%rbp)
	jg	.L2
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %edx
	movsbl	-28(%rbp), %eax
	cmpl	%eax, %edx
	jne	.L3
	addl	$1, -8(%rbp)
	jmp	.L4
.L3:
	movl	-4(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	cmpb	$1, -28(%rbp)
	jne	.L5
	movl	$2, %edx
	jmp	.L6
.L5:
	movl	$1, %edx
.L6:
	cmpl	%eax, %edx
	jne	.L4
	subl	$1, -8(%rbp)
.L4:
	addl	$1, -4(%rbp)
	jmp	.L7
.L2:
	movl	-8(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	_Z11countColorsPhc, .-_Z11countColorsPhc
	.ident	"GCC: (GNU) 7.3.0"
	.section	.note.GNU-stack,"",@progbits
