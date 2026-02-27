/**
 * IDENTIA Authentication & Session Management
 */

const Auth = {
    /**
     * Handle Login Submission
     */
    async login(email, password) {
        try {
            const result = await IDENTIA_API.post('/auth/login', { email, password });

            if (result.token) {
                localStorage.setItem('id_token', result.token);
                localStorage.setItem('id_user', JSON.stringify(result.user));
                window.location.href = '/dashboard';
            }
        } catch (error) {
            this.showError('Invalid credentials or server error.');
        }
    },

    /**
     * Handle Logout
     */
    logout() {
        localStorage.removeItem('id_token');
        localStorage.removeItem('id_user');
        window.location.href = '/login';
    },

    /**
     * UI Feedback
     */
    showError(msg) {
        const errorEl = document.getElementById('login-error');
        if (errorEl) {
            errorEl.textContent = msg;
            errorEl.classList.remove('hidden');
        } else {
            alert(msg);
        }
    }
};

window.IDENTIA_AUTH = Auth;
