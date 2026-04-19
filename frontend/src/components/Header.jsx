import { Bug } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-slate-800 border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-8 py-6">
        <div className="flex items-center gap-4">
          <Bug size={32} className="text-indigo-500" />
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">
            AI Code Debugger
          </h1>
        </div>
        
        <p className="text-slate-400 text-sm mt-1 ml-12">
          Powered by Fine-tuned CodeGen-350M
        </p>
      </div>
    </header>
  );
};

export default Header;