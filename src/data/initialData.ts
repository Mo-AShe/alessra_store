import { Product, Customer, Transaction, User, ShopSettings } from '../types';

export const initialProducts: Product[] = [];

export const initialCustomers: Customer[] = [];

export const initialTransactions: Transaction[] = [];

export const initialUsers: User[] = [
  {
    id: 1,
    email: 'admin@al-esraa.com',
    password: 'admin123',
    name: 'أحمد إبراهيم',
    role: 'مدير النظام',
    roleCode: 'admin',
    permissions: ['dashboard', 'inventory', 'pos', 'customers', 'reports', 'settings', 'profile'],
    status: 'active'
  },
  {
    id: 2,
    email: 'employee@al-esraa.com',
    password: 'emp123',
    name: 'محمد علي',
    role: 'موظف',
    roleCode: 'employee',
    permissions: ['dashboard', 'pos', 'customers', 'profile'],
    status: 'active'
  },
  {
    id: 3,
    email: 'inventory@al-esraa.com',
    password: 'inv123',
    name: 'خالد سعيد',
    role: 'موظف',
    roleCode: 'employee',
    permissions: ['dashboard', 'pos', 'customers', 'profile'],
    status: 'inactive'
  }
];

export const initialSettings: ShopSettings = {
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
