/**
 * IDENTIA API Client
 * Centralized fetch wrapper for REST API communication.
 */

const API_CONFIG = {
    BASE_URL: '/api', // Can be adjusted for cross-origin if needed
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};

const API = {
    /**
     * Get the authorization header from local storage (JWT)
     */
    getAuthHeader() {
        const token = localStorage.getItem('id_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    },

    /**
     * Internal request wrapper
     */
    async request(endpoint, options = {}) {
        const url = `${API_CONFIG.BASE_URL}${endpoint}`;
        const headers = {
            ...API_CONFIG.HEADERS,
            ...this.getAuthHeader(),
            ...options.headers
        };

        try {
            const response = await fetch(url, { ...options, headers });
            
            // Handle 401 Unauthorized (invalid token)
            if (response.status === 401) {
                window.location.href = '/login?error=expired';
                return;
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Failed:', error);
            throw error;
        }
    },

    // Convenience methods
    get: (endpoint) => API.request(endpoint, { method: 'GET' }),
    post: (endpoint, data) => API.request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: (endpoint, data) => API.request(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (endpoint) => API.request(endpoint, { method: 'DELETE' })
};

// Global export for use in specialized JS files
window.IDENTIA_API = API;
