// marketplace-frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Lazy load views to improve initial load performance
const HomeView = () => import('../views/Home/Home.vue');
// const ProductsView = () => import('../views/Products/Products.vue');
// const ProductDetailView = () => import('../views/ProductDetail/ProductDetail.vue');
const LoginView = () => import('../views/Auth/Login.vue');
// const RegisterView = () => import('../views/Auth/Register.vue');
// const UserProfileView = () => import('../views/UserProfile/UserProfile.vue');
// const NotFoundView = () => import('../views/NotFound.vue'); // Or a generic 404 page

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  // {
  //   path: '/products',
  //   name: 'Products',
  //   component: ProductsView
  // },
  // {
  //   path: '/products/:id', // Dynamic segment for product ID
  //   name: 'ProductDetail',
  //   component: ProductDetailView,
  //   props: true // Pass route params as props to the component
  // },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false } // Custom meta field for auth
  },
  // {
  //   path: '/register',
  //   name: 'Register',
  //   component: RegisterView,
  //   meta: { requiresAuth: false }
  // },
  // {
  //   path: '/profile',
  //   name: 'UserProfile',
  //   component: UserProfileView,
  //   meta: { requiresAuth: true } // This route requires authentication
  // },
  // // Catch all 404 route - should be the last one
  // {
  //   path: '/:catchAll(.*)',
  //   name: 'NotFound',
  //   component: NotFoundView
  // }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Uses HTML5 History API (clean URLs)
  routes: routes // short for `routes: routes`
});

// Navigation Guard (Global beforeEach)
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('userToken'); // Simple check, adjust as needed

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    // If user is authenticated and tries to access login/register, redirect to profile or home
    next({ name: 'UserProfile' }); // Or next({ name: 'Home' });
  } else {
    // Continue to the route
    next();
  }
});

export default router;
