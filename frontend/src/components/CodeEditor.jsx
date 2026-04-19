import { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Trash2 } from 'lucide-react';

const CodeEditor = ({ onDebug, isLoading }) => {
  // State: stores the code user types
  const [code, setCode] = useState(`def greet():
    print("Hello World")

greet()`);

  // Handler: called when "Debug" button clicked
  const handleDebug = () => {
    if (code.trim()) {
      onDebug(code);
    }
  };

  // Handler: called when "Clear" button clicked
  const handleClear = () => {
    setCode('');
  };

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      {/* Header with title and buttons */}
      <div className="flex justify-between items-center px-6 py-4 border-b border-slate-700 bg-slate-900">
        <h2 className="text-xl font-semibold text-white">Your Code</h2>
        
        <div className="flex gap-3">
          {/* Clear Button */}
          <button 
            onClick={handleClear}
            disabled={isLoading}
            className="flex items-center gap-2 px-4 py-2 bg-transparent border border-slate-600 text-slate-300 rounded-lg hover:bg-slate-700 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Trash2 size={18} />
            Clear
          </button>
          
          {/* Debug Button */}
          <button 
            onClick={handleDebug}
            disabled={isLoading || !code.trim()}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play size={18} />
            {isLoading ? 'Debugging...' : 'Debug Code'}
          </button>
        </div>
      </div>
      
      {/* Monaco Editor */}
      <div className="p-4">
        <Editor
          height="500px"
          defaultLanguage="python"
          theme="vs-dark"
          value={code}
          onChange={(value) => setCode(value || '')}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
          }}
        />
      </div>
    </div>
  );
};

export default CodeEditor;