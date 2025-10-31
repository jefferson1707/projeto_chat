// ===== FUNÇÕES GERAIS =====

/**
 * Mostra mensagem de loading
 */
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<div class="loading"></div> Processando...';
    button.disabled = true;
    return originalText;
}

/**
 * Restaura botão após loading
 */
function hideLoading(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

/**
 * Mostra toast de notificação
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);

    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

/**
 * Formata data para exibição
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
        return 'Hoje ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 2) {
        return 'Ontem ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays <= 7) {
        return date.toLocaleDateString('pt-BR', { weekday: 'long', hour: '2-digit', minute: '2-digit' });
    } else {
        return date.toLocaleDateString('pt-BR');
    }
}

/**
 * Valida formulário de registro
 */
function validateRegisterForm() {
    const password = document.querySelector('input[name="password"]');
    const confirmPassword = document.querySelector('input[name="confirm_password"]');

    if (password && confirmPassword && password.value !== confirmPassword.value) {
        showToast('As senhas não coincidem!', 'danger');
        return false;
    }

    return true;
}

/**
 * Rolagem automática para o final do chat
 */
function scrollToBottom(container) {
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}


/**
 * Alterna entre mostrar e ocultar senha - VERSÃO SIMPLIFICADA
 */
function togglePasswordVisibility(button) {
    const inputGroup = button.closest('.input-group');
    const passwordField = inputGroup.querySelector('input[type="password"], input[type="text"]');
    const eyeEmoji = button.querySelector('.eye-emoji');

    if (passwordField && eyeEmoji) {
        // Alterna entre password e text
        const isPassword = passwordField.type === 'password';
        passwordField.type = isPassword ? 'text' : 'password';

        // Alterna o emoji
        eyeEmoji.textContent = isPassword ? '🙈' : '👁️';

        // Feedback visual
        button.classList.toggle('active', isPassword);

        // Foca de volta no campo
        passwordField.focus();
    }
}

// Configuração dos botões
document.addEventListener('DOMContentLoaded', function () {
    // Configura botões de mostrar/ocultar senha
    const toggleButtons = document.querySelectorAll('.password-toggle-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function () {
            togglePasswordVisibility(this);
        });
    });

    // Outros event listeners existentes...
    document.querySelectorAll('.timestamp').forEach(element => {
        const dateString = element.getAttribute('data-timestamp');
        if (dateString) {
            element.textContent = formatDate(dateString);
        }
    });

    // ... resto do código existente
});

// ===== FUNÇÕES PARA CHAT =====

/**
 * Envia mensagem via AJAX (para implementação futura)
 */
async function sendMessage(conversationId, message) {
    try {
        const response = await fetch(`/minha-conta/conversa/${conversationId}/enviar-mensagem`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: message })
        });

        return await response.json();
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        throw error;
    }
}