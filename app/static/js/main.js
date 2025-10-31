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
 * Alterna entre mostrar e ocultar senha com feedback visual
 */
function togglePasswordVisibility(passwordFieldId, toggleButtonId, toggleIconId) {
    const passwordField = document.getElementById(passwordFieldId);
    const toggleButton = document.getElementById(toggleButtonId);
    const toggleIcon = document.getElementById(toggleIconId);
    
    if (passwordField && toggleIcon && toggleButton) {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        // Alterna o ícone do olho e estados visuais
        if (type === 'text') {
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
            toggleButton.setAttribute('aria-label', 'Ocultar senha');
            toggleButton.classList.add('active');
            
            // Feedback visual temporário
            toggleButton.style.backgroundColor = 'var(--gray-100)';
            setTimeout(() => {
                toggleButton.style.backgroundColor = '';
            }, 300);
            
        } else {
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
            toggleButton.setAttribute('aria-label', 'Mostrar senha');
            toggleButton.classList.remove('active');
        }
        
        // Foca de volta no campo de senha para continuar digitando
        passwordField.focus();
    }
}

// ===== EVENT LISTENERS =====

document.addEventListener('DOMContentLoaded', function() {
    // Formata todas as datas na página
    document.querySelectorAll('.timestamp').forEach(element => {
        const dateString = element.getAttribute('data-timestamp');
        if (dateString) {
            element.textContent = formatDate(dateString);
        }
    });
    
    // Validação de formulários
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            if (!validateRegisterForm()) {
                e.preventDefault();
            }
        });
    }
    
    // Rolagem automática em chats (apenas se não houver script específico)
    const chatContainer = document.querySelector('.chat-messages');
    if (chatContainer && !document.querySelector('#chat-form')) {
        scrollToBottom(chatContainer);
    }
    
    // Efeitos hover em cards
    document.querySelectorAll('.card.clickable').forEach(card => {
        card.addEventListener('click', function() {
            window.location.href = this.getAttribute('data-href');
        });
    });
    
    // Configura botões de mostrar/ocultar senha
    const togglePasswordButtons = document.querySelectorAll('.password-toggle-btn');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = this.closest('.input-group').querySelector('input[type="password"], input[type="text"]');
            const passwordFieldId = passwordField.id;
            const toggleButtonId = this.id;
            const toggleIconId = this.querySelector('i').id;
            
            togglePasswordVisibility(passwordFieldId, toggleButtonId, toggleIconId);
        });
        
        // Adiciona suporte a teclado (Enter e Space)
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
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