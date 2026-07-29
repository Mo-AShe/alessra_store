import React, { useState } from 'react';
import { useStore } from '../context/StoreContext';
import { UserRole } from '../types';

export const LoginView: React.FC = () => {
  const { login } = useStore();

  const [selectedRole, setSelectedRole] = useState<UserRole>('admin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleRoleSelect = (role: UserRole) => {
    setSelectedRole(role);
    setErrorMsg('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setIsSubmitting(true);

    try {
      const success = await login(email, password);
      if (!success) {
        setErrorMsg('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة');
      }
    } catch (err) {
      setErrorMsg('❌ متعذر الاتصال بقاعدة البيانات، يرجى المحاولة لاحقاً');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f1a3a] via-[#1a2a6c] to-[#2a3f8f] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Floating background graphic */}
      <div className="absolute -top-[50%] -left-[50%] w-[200%] h-[200%] bg-[radial-gradient(circle_at_30%_50%,rgba(255,215,0,0.03),transparent_50%),radial-gradient(circle_at_70%_80%,rgba(255,215,0,0.02),transparent_50%)] animate-bg-float pointer-events-none"></div>

      {/* Login Card */}
      <div className="bg-white/5 backdrop-blur-2xl rounded-3xl p-8 sm:p-11 max-w-md w-full border border-white/10 shadow-2xl shadow-black/50 relative z-10 animate-slide-up">
        
        {/* DB Connection Badge */}
        <div className="flex justify-center mb-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>متصل بقاعدة البيانات</span>
          </div>
        </div>

        {/* Logo Section */}
        <div className="text-center mb-6">
          <div className="w-[72px] h-[72px] bg-gradient-to-br from-[#fdd835] to-[#f9a825] rounded-2xl flex items-center justify-center text-3xl text-[#0f1a3a] mx-auto mb-3 shadow-lg shadow-[#fdd835]/25 relative">
            <i className="fas fa-wrench"></i>
            <span className="absolute -bottom-1 -right-1 text-base">🇪🇬</span>
          </div>
          <div className="text-3xl font-black text-white tracking-wide">
            محل <span className="text-[#fdd835]">الإسراء</span>
          </div>
          <div className="text-xs text-white/50 font-medium tracking-widest mt-1">
            ✦ أدوات السباكة ✦
          </div>
        </div>

        <div className="text-center text-white/70 text-sm mb-6 font-light">
          👋 مرحباً بك! <strong className="text-white font-bold">سجل الدخول</strong> لإدارة النظام
        </div>

        {/* Error message */}
        {errorMsg && (
          <div className="bg-red-500/15 border border-red-500/30 text-red-300 p-3 rounded-xl text-sm mb-5 flex items-center gap-2 animate-fade-in">
            <i className="fas fa-exclamation-circle text-red-400"></i>
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Role selector */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            <div
              onClick={() => handleRoleSelect('admin')}
              className={`p-3.5 rounded-2xl border-2 text-center cursor-pointer transition-all ${
                selectedRole === 'admin'
                  ? 'border-[#fdd835] bg-[#fdd835]/10 text-[#fdd835] shadow-md shadow-[#fdd835]/10'
                  : 'border-white/5 bg-white/5 text-white/40 hover:bg-white/10'
              }`}
            >
              <div className="text-sm font-bold flex items-center justify-center gap-1.5">
                <span>👑</span>
                <span>مدير النظام</span>
              </div>
              <div className="text-[11px] opacity-70 mt-0.5">صلاحيات كاملة</div>
            </div>

            <div
              onClick={() => handleRoleSelect('employee')}
              className={`p-3.5 rounded-2xl border-2 text-center cursor-pointer transition-all ${
                selectedRole === 'employee'
                  ? 'border-[#fdd835] bg-[#fdd835]/10 text-[#fdd835] shadow-md shadow-[#fdd835]/10'
                  : 'border-white/5 bg-white/5 text-white/40 hover:bg-white/10'
              }`}
            >
              <div className="text-sm font-bold flex items-center justify-center gap-1.5">
                <span>👤</span>
                <span>موظف المبيعات</span>
              </div>
              <div className="text-[11px] opacity-70 mt-0.5">مبيعات وعملاء</div>
            </div>
          </div>

          {/* Email input */}
          <div className="mb-4">
            <label className="block text-white/60 text-xs font-semibold mb-1">
              📧 البريد الإلكتروني
            </label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@email.com"
                className="w-full py-3.5 pr-12 pl-4 rounded-xl border border-white/10 bg-white/5 text-white placeholder-white/20 text-sm focus:outline-none focus:border-[#fdd835]/50 focus:bg-white/10 transition-all"
              />
              <i className="fas fa-envelope absolute right-4 top-1/2 -translate-y-1/2 text-white/30 text-base"></i>
            </div>
          </div>

          {/* Password input */}
          <div className="mb-5">
            <label className="block text-white/60 text-xs font-semibold mb-1">
              🔑 كلمة المرور
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full py-3.5 pr-12 pl-12 rounded-xl border border-white/10 bg-white/5 text-white placeholder-white/20 text-sm focus:outline-none focus:border-[#fdd835]/50 focus:bg-white/10 transition-all"
              />
              <i className="fas fa-lock absolute right-4 top-1/2 -translate-y-1/2 text-white/30 text-base"></i>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40 hover:text-white text-xs cursor-pointer"
              >
                <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
              </button>
            </div>
          </div>

          {/* Submit button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#fdd835] to-[#f9a825] text-[#0f1a3a] font-black text-lg shadow-lg shadow-[#fdd835]/20 hover:shadow-xl hover:shadow-[#fdd835]/30 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 transition-all flex items-center justify-center gap-2 cursor-pointer mb-4"
          >
            {isSubmitting ? (
              <>
                <i className="fas fa-circle-notch fa-spin"></i>
                <span>جاري التحقق...</span>
              </>
            ) : (
              <>
                <i className="fas fa-sign-in-alt"></i>
                <span>تسجيل الدخول</span>
              </>
            )}
          </button>
        </form>

        <div className="text-center mt-6 text-white/30 text-xs tracking-wider">
          محل الإسراء لأدوات السباكة © {new Date().getFullYear()} — نظام إدارة المتجر
        </div>
      </div>
    </div>
  );
};
