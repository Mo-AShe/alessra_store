// src/context/StoreContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

// Types
export interface Product {
  id: number;
  name: string;
  code: string;
  category: string;
  buyPrice: number;
  sellPrice: number;
  stock: number;
  minStock: number;
}

export interface Customer {
  id: number;
  name: string;
  phone: string;
  totalPurchases: number;
  paid: number;
  status: string;
}

export interface Transaction {
  id: number;
  invoiceNo: string;
  time: string;
  date: string;
  customerName: string;
  productName: string;
  amount: number;
  totalQuantity?: number;
  status: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  roleCode: string;
  permissions: string[];
  status: string;
}

export interface ShopSettings {
  shop: {
    name: string;
    address: string;
    phone: string;
    email: string;
  };
  invoice: {
    start: number;
    discount: number;
    tax: number;
    copies: number;
    showTax: boolean;
    showDiscount: boolean;
  };
  currency: string;
  dateFormat: string;
  timezone: string;
}

export interface UserSession {
  user: User;
  loginTime: string;
}

export interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

export interface CartItem {
  id: number;
  name: string;
  price: number;
  qty: number;
  category?: string;
  maxStock?: number;
}

export type ViewPage = 
  | 'dashboard'
  | 'products'
  | 'customers'
  | 'transactions'
  | 'users'
  | 'settings'
  | 'profile'
  | 'pos';

// API Configuration - Direct connection to your backend
const API_URL = import.meta.env?.VITE_API_URL || 'https://alessra-store.vercel.app';

const apiFetch = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_URL}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error ${response.status}:`, errorText);
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Initial Data (fallback if backend fails)
const initialProducts: Product[] = [
  { id: 1, name: 'خلاط مياه حوض نيكل استانلس', code: 'P-101', category: 'خلاطات', buyPrice: 450, sellPrice: 650, stock: 25, minStock: 5 },
  { id: 2, name: 'محبس دفن 3/4 بوصة إيطالي', code: 'P-102', category: 'محابس ومحولات', buyPrice: 85, sellPrice: 130, stock: 40, minStock: 10 },
];

const initialCustomers: Customer[] = [
  { id: 1, name: 'الشركة الهندسية للمقاولات', phone: '010-1234-5678', totalPurchases: 0, paid: 0, status: 'paid' },
  { id: 2, name: 'معلم أحمد السباك', phone: '011-9876-5432', totalPurchases: 0, paid: 0, status: 'paid' },
];

const initialUsers: User[] = [
  { id: 1, name: 'أحمد إبراهيم', email: 'admin@al-esraa.com', role: 'مدير النظام', roleCode: 'admin', permissions: ['dashboard', 'inventory', 'pos', 'customers', 'reports', 'settings', 'profile'], status: 'active' },
  { id: 2, name: 'محمد علي', email: 'employee@al-esraa.com', role: 'موظف', roleCode: 'employee', permissions: ['dashboard', 'pos', 'customers', 'profile'], status: 'active' },
];

const initialSettings: ShopSettings = {
  shop: {
    name: 'محل الاسراء لأدوات السباكة',
    address: 'مصر - القاهرة - مدينة نصر',
    phone: '012-3456-7890',
    email: 'info@al-esraa.com'
  },
  invoice: {
    start: 1,
    discount: 0,
    tax: 14,
    copies: 1,
    showTax: true,
    showDiscount: true
  },
  currency: 'EGP',
  dateFormat: 'ar-EG',
  timezone: 'Africa/Cairo'
};

interface StoreContextType {
  currentUserSession: UserSession | null;
  currentPage: ViewPage;
  setCurrentPage: (page: ViewPage) => void;
  products: Product[];
  customers: Customer[];
  transactions: Transaction[];
  users: User[];
  settings: ShopSettings;
  toasts: ToastMessage[];
  showToast: (message: string, type?: 'success' | 'error' | 'info') => void;
  removeToast: (id: string) => void;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  addProduct: (product: Omit<Product, 'id'>) => Promise<void>;
  updateProduct: (product: Product) => Promise<void>;
  deleteProduct: (id: number) => Promise<void>;
  addCustomer: (customer: Omit<Customer, 'id'>) => Promise<void>;
  updateCustomer: (customer: Customer) => Promise<void>;
  deleteCustomer: (id: number) => Promise<void>;
  processCheckout: (cart: CartItem[], discount: number, selectedCustomerId?: number) => Promise<{ success: boolean; invoiceNo: string }>;
  addUser: (user: Omit<User, 'id'>) => Promise<boolean>;
  updateUser: (user: User) => Promise<boolean>;
  toggleUserStatus: (id: number) => Promise<void>;
  updateSettings: (newSettings: ShopSettings) => Promise<void>;
  resetSettingsToDefault: () => void;
  updateUserProfile: (name: string, phone: string) => Promise<void>;
  changeUserPassword: (currentPass: string, newPass: string) => Promise<boolean>;
  refreshStoreData: () => void;
  getSalesReport: (startDate?: string, endDate?: string) => any;
  getTopProducts: (limit?: number) => any[];
  getCustomerReport: () => any[];
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

export const StoreProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentPage, setCurrentPage] = useState<ViewPage>('dashboard');
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  
  const [currentUserSession, setCurrentUserSession] = useState<UserSession | null>(() => {
    const saved = localStorage.getItem('userSession');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) { return null; }
    }
    return { user: initialUsers[0], loginTime: new Date().toISOString() };
  });

  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [customers, setCustomers] = useState<Customer[]>(initialCustomers);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [users, setUsers] = useState<User[]>(initialUsers);
  const [settings, setSettings] = useState<ShopSettings>(initialSettings);

  const showToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    const id = Date.now().toString() + Math.random().toString().slice(2, 6);
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => removeToast(id), 4000);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  // Load data from backend
  const loadDataFromBackend = async () => {
    try {
      console.log('🔄 Loading data from backend...');
      
      // Seed database if needed
      await apiFetch('/api/seed', { method: 'POST' }).catch(() => {});
      
      // Fetch products
      const productsRes = await apiFetch('/api/products');
      if (productsRes.ok) {
        const data = await productsRes.json();
        if (Array.isArray(data) && data.length > 0) {
          setProducts(data);
        }
      }
      
      // Fetch customers
      const customersRes = await apiFetch('/api/customers');
      if (customersRes.ok) {
        const data = await customersRes.json();
        if (Array.isArray(data) && data.length > 0) {
          setCustomers(data);
        }
      }
      
      // Fetch transactions
      const transactionsRes = await apiFetch('/api/transactions');
      if (transactionsRes.ok) {
        const data = await transactionsRes.json();
        if (Array.isArray(data)) {
          setTransactions(data);
        }
      }
      
      // Fetch users
      const usersRes = await apiFetch('/api/users');
      if (usersRes.ok) {
        const data = await usersRes.json();
        if (Array.isArray(data) && data.length > 0) {
          setUsers(data);
        }
      }
      
      // Fetch settings
      const settingsRes = await apiFetch('/api/settings');
      if (settingsRes.ok) {
        const data = await settingsRes.json();
        if (data && data.shop) {
          setSettings(data);
        }
      }
      
      console.log('✅ Data loaded successfully');
    } catch (err) {
      console.warn('⚠️ Backend sync warning, using local state:', err);
    }
  };

  useEffect(() => {
    loadDataFromBackend();
  }, []);

  // Login
  const login = async (email: string, pass: string): Promise<boolean> => {
    try {
      console.log('🔐 Attempting login:', email);
      const res = await apiFetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password: pass })
      });
      
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.user) {
          const session: UserSession = {
            user: data.user,
            loginTime: new Date().toISOString()
          };
          setCurrentUserSession(session);
          localStorage.setItem('userSession', JSON.stringify(session));
          showToast(`مرحباً بك ${data.user.name}!`, 'success');
          setCurrentPage('dashboard');
          return true;
        }
      }
    } catch (err) {
      console.warn('Backend login failed:', err);
    }

    showToast('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة', 'error');
    return false;
  };

  const logout = () => {
    setCurrentUserSession(null);
    localStorage.removeItem('userSession');
    showToast('تم تسجيل الخروج', 'info');
  };

  // Product CRUD
  const addProduct = async (p: Omit<Product, 'id'>) => {
    try {
      const res = await apiFetch('/api/products', {
        method: 'POST',
        body: JSON.stringify(p)
      });
      if (res.ok) {
        const created = await res.json();
        setProducts(prev => [created, ...prev]);
        showToast(`✅ تم إضافة المنتج "${created.name}"`, 'success');
        return;
      }
    } catch (e) {}
    
    // Fallback
    const newId = products.length > 0 ? Math.max(...products.map(item => item.id)) + 1 : 1;
    const newProduct = { ...p, id: newId };
    setProducts(prev => [newProduct, ...prev]);
    showToast(`✅ تم إضافة المنتج "${p.name}" (محلياً)`, 'success');
  };

  const updateProduct = async (updated: Product) => {
    try {
      const res = await apiFetch(`/api/products/${updated.id}`, {
        method: 'PUT',
        body: JSON.stringify(updated)
      });
      if (res.ok) {
        const data = await res.json();
        setProducts(prev => prev.map(p => p.id === data.id ? data : p));
        showToast(`✅ تم تحديث المنتج "${data.name}"`, 'success');
        return;
      }
    } catch (e) {}
    
    setProducts(prev => prev.map(p => p.id === updated.id ? updated : p));
    showToast(`✅ تم تحديث المنتج "${updated.name}" (محلياً)`, 'success');
  };

  const deleteProduct = async (id: number) => {
    try {
      await apiFetch(`/api/products/${id}`, { method: 'DELETE' });
    } catch (e) {}
    const target = products.find(p => p.id === id);
    setProducts(prev => prev.filter(p => p.id !== id));
    showToast(`🗑️ تم حذف المنتج "${target?.name || ''}"`, 'info');
  };

  // Customer CRUD
  const addCustomer = async (c: Omit<Customer, 'id'>) => {
    try {
      const res = await apiFetch('/api/customers', {
        method: 'POST',
        body: JSON.stringify(c)
      });
      if (res.ok) {
        const created = await res.json();
        setCustomers(prev => [created, ...prev]);
        showToast(`👤 تم إضافة العميل "${created.name}"`, 'success');
        return;
      }
    } catch (e) {}
    
    const newId = customers.length > 0 ? Math.max(...customers.map(item => item.id)) + 1 : 1;
    setCustomers(prev => [{ ...c, id: newId }, ...prev]);
    showToast(`👤 تم إضافة العميل "${c.name}" (محلياً)`, 'success');
  };

  const updateCustomer = async (updated: Customer) => {
    try {
      const res = await apiFetch(`/api/customers/${updated.id}`, {
        method: 'PUT',
        body: JSON.stringify(updated)
      });
      if (res.ok) {
        const data = await res.json();
        setCustomers(prev => prev.map(c => c.id === data.id ? data : c));
        showToast(`✅ تم تحديث العميل "${data.name}"`, 'success');
        return;
      }
    } catch (e) {}
    
    setCustomers(prev => prev.map(c => c.id === updated.id ? updated : c));
    showToast(`✅ تم تحديث العميل "${updated.name}" (محلياً)`, 'success');
  };

  const deleteCustomer = async (id: number) => {
    try {
      await apiFetch(`/api/customers/${id}`, { method: 'DELETE' });
    } catch (e) {}
    const target = customers.find(c => c.id === id);
    setCustomers(prev => prev.filter(c => c.id !== id));
    showToast(`🗑️ تم حذف العميل "${target?.name || ''}"`, 'info');
  };

  // POS Checkout
  const processCheckout = async (cart: CartItem[], discount: number, selectedCustomerId?: number) => {
    if (cart.length === 0) {
      showToast('⚠️ السلة فارغة!', 'error');
      return { success: false, invoiceNo: '' };
    }

    try {
      const res = await apiFetch('/api/checkout', {
        method: 'POST',
        body: JSON.stringify({ cart, discount, selectedCustomerId })
      });
      
      if (res.ok) {
        const data = await res.json();
        if (data.success) {
          showToast(`✅ تم إصدار الفاتورة #${data.invoiceNo}`, 'success');
          // Refresh data to get latest
          await loadDataFromBackend();
          return { success: true, invoiceNo: data.invoiceNo };
        }
      }
    } catch (e) {
      console.error('Checkout error:', e);
    }

    showToast('❌ فشل إتمام عملية البيع', 'error');
    return { success: false, invoiceNo: '' };
  };

  // User management
  const addUser = async (u: Omit<User, 'id'>): Promise<boolean> => {
    try {
      const res = await apiFetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(u)
      });
      if (res.ok) {
        const created = await res.json();
        setUsers(prev => [...prev, created]);
        showToast(`✅ تم إضافة المستخدم "${created.name}"`, 'success');
        return true;
      }
    } catch (e) {}
    
    showToast('❌ فشل إضافة المستخدم', 'error');
    return false;
  };

  const updateUser = async (u: User): Promise<boolean> => {
    try {
      const res = await apiFetch(`/api/users/${u.id}`, {
        method: 'PUT',
        body: JSON.stringify(u)
      });
      if (res.ok) {
        const updated = await res.json();
        setUsers(prev => prev.map(user => user.id === updated.id ? updated : user));
        showToast(`✅ تم تحديث المستخدم "${updated.name}"`, 'success');
        return true;
      }
    } catch (e) {}
    
    showToast('❌ فشل تحديث المستخدم', 'error');
    return false;
  };

  const toggleUserStatus = async (id: number) => {
    try {
      const user = users.find(u => u.id === id);
      if (!user) return;
      
      const newStatus = user.status === 'active' ? 'inactive' : 'active';
      await apiFetch(`/api/users/${id}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status: newStatus })
      });
      
      setUsers(prev => prev.map(u => {
        if (u.id === id) {
          showToast(`🔄 تم تغيير حالة ${u.name}`, 'info');
          return { ...u, status: newStatus };
        }
        return u;
      }));
    } catch (e) {
      showToast('❌ فشل تغيير حالة المستخدم', 'error');
    }
  };

  // Settings
  const updateSettings = async (newSettings: ShopSettings) => {
    try {
      await apiFetch('/api/settings', {
        method: 'PUT',
        body: JSON.stringify(newSettings)
      });
      setSettings(newSettings);
      showToast('✅ تم حفظ الإعدادات', 'success');
    } catch (e) {
      setSettings(newSettings);
      showToast('✅ تم حفظ الإعدادات (محلياً)', 'success');
    }
  };

  const resetSettingsToDefault = () => {
    setSettings(initialSettings);
    showToast('🔄 تم استعادة الإعدادات الافتراضية', 'info');
  };

  // Profile
  const updateUserProfile = async (name: string, phone: string) => {
    if (!currentUserSession) return;
    
    try {
      await apiFetch(`/api/users/${currentUserSession.user.id}/profile`, {
        method: 'PUT',
        body: JSON.stringify({ name, phone })
      });
      
      const updatedUser = { ...currentUserSession.user, name };
      const updatedSession = { ...currentUserSession, user: updatedUser };
      setCurrentUserSession(updatedSession);
      localStorage.setItem('userSession', JSON.stringify(updatedSession));
      setUsers(prev => prev.map(u => u.id === updatedUser.id ? updatedUser : u));
      showToast('✅ تم حفظ الملف الشخصي', 'success');
    } catch (e) {
      showToast('❌ فشل حفظ الملف الشخصي', 'error');
    }
  };

  const changeUserPassword = async (currentPass: string, newPass: string): Promise<boolean> => {
    if (!currentUserSession) return false;
    
    try {
      await apiFetch(`/api/users/${currentUserSession.user.id}/password`, {
        method: 'PUT',
        body: JSON.stringify({ newPassword: newPass })
      });
      
      showToast('✅ تم تغيير كلمة المرور', 'success');
      return true;
    } catch (e) {
      showToast('❌ فشل تغيير كلمة المرور', 'error');
      return false;
    }
  };

  const refreshStoreData = () => {
    showToast('🔄 جاري التحديث...', 'info');
    loadDataFromBackend().then(() => {
      showToast('✅ تم تحديث البيانات', 'success');
    });
  };

  // Reports
  const getSalesReport = (startDate?: string, endDate?: string) => {
    let filtered = [...transactions];
    if (startDate) filtered = filtered.filter(t => t.date >= startDate);
    if (endDate) filtered = filtered.filter(t => t.date <= endDate);
    
    return {
      totalSales: filtered.reduce((sum, t) => sum + t.amount, 0),
      averageOrder: filtered.length > 0 ? filtered.reduce((sum, t) => sum + t.amount, 0) / filtered.length : 0,
      totalOrders: filtered.length,
      transactions: filtered
    };
  };

  const getTopProducts = (limit: number = 5) => {
    const productSales = new Map<number, { name: string; total: number; qty: number }>();
    transactions.forEach(t => {
      const product = products.find(p => t.productName?.includes(p.name));
      if (product) {
        const existing = productSales.get(product.id);
        if (existing) {
          existing.total += t.amount;
          existing.qty += 1;
        } else {
          productSales.set(product.id, { name: product.name, total: t.amount, qty: 1 });
        }
      }
    });
    return Array.from(productSales.values()).sort((a, b) => b.total - a.total).slice(0, limit);
  };

  const getCustomerReport = () => {
    return customers.map(c => ({
      ...c,
      orderCount: transactions.filter(t => t.customerName === c.name).length,
      averageOrder: c.totalPurchases / (transactions.filter(t => t.customerName === c.name).length || 1)
    }));
  };

  return (
    <StoreContext.Provider value={{
      currentUserSession,
      currentPage,
      setCurrentPage,
      products,
      customers,
      transactions,
      users,
      settings,
      toasts,
      showToast,
      removeToast,
      login,
      logout,
      addProduct,
      updateProduct,
      deleteProduct,
      addCustomer,
      updateCustomer,
      deleteCustomer,
      processCheckout,
      addUser,
      updateUser,
      toggleUserStatus,
      updateSettings,
      resetSettingsToDefault,
      updateUserProfile,
      changeUserPassword,
      refreshStoreData,
      getSalesReport,
      getTopProducts,
      getCustomerReport
    }}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => {
  const context = useContext(StoreContext);
  if (!context) throw new Error('useStore must be used within StoreProvider');
  return context;
};