import { defineStore } from 'pinia';
import api from '@/services/api'; // Assuming your api service is set up

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('userToken') || null, // Persist token
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
  },
  actions: {
    async login(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.post('/auth/login', credentials);
        this.token = response.data.token;
        this.user = response.data.user;
        localStorage.setItem('userToken', this.token);
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`; // Set token for future requests
        return true; // Indicate success
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed.';
        console.error('Login error:', error);
        return false; // Indicate failure
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('userToken');
      delete api.defaults.headers.common['Authorization'];
      // Redirect to login or home page after logout
      // router.push({ name: 'Login' }); // If you import router directly
    },
    // Action to fetch user details after successful login or on app load
    async fetchUser() {
      if (!this.token) return;
      this.loading = true;
      try {
        const response = await api.get('/api/v1/users/me'); // Endpoint to get current user
        this.user = response.data.user;
      } catch (error) {
        console.error('Failed to fetch user:', error);
        this.logout(); // Logout if token is invalid
      } finally {
        this.loading = false;
      }
    }
  },
});
