import { AlertCircle, CheckCircle, Lightbulb, Code } from 'lucide-react';
import Editor from '@monaco-editor/react';

const Result = ({ result }) => {
  // If no results yet, show empty state
  if (!result) {
    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 min-h-[500px] flex items-center justify-center">
        <div className="text-center text-slate-400">
          <Code size={64} className="mx-auto mb-4 opacity-30" />
          <h3 className="text-xl font-semibold text-white mb-2">
            No Results Yet
          </h3>
          <p>Submit your code to see AI-powered debugging analysis</p>
        </div>
      </div>
    );
  }

  // Show results
  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-700 bg-slate-900">
        <h2 className="text-xl font-semibold text-white">Analysis Results</h2>
      </div>

      <div className="p-6 space-y-4">
        {/* Error Section */}
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center gap-3 mb-3">
            <AlertCircle size={20} className="text-red-500" />
            <h3 className="font-semibold text-white">Error Detected</h3>
          </div>
          <code className="block bg-red-950/50 border-l-4 border-red-500 px-4 py-3 rounded text-red-300 font-mono text-sm">
            {result.error || 'No error detected'}
          </code>
        </div>

        {/* Root Cause Section */}
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center gap-3 mb-3">
            <Lightbulb size={20} className="text-yellow-500" />
            <h3 className="font-semibold text-white">Root Cause</h3>
          </div>
          <p className="text-slate-300 leading-relaxed">
            {result.root_cause || 'N/A'}
          </p>
        </div>

        {/* Best Practice Section */}
        {result.best_practice && (
          <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
            <div className="flex items-center gap-3 mb-3">
              <CheckCircle size={20} className="text-green-500" />
              <h3 className="font-semibold text-white">Best Practice</h3>
            </div>
            <p className="text-slate-300 leading-relaxed">
              {result.best_practice}
            </p>
          </div>
        )}

        {/* Fixed Code Section */}
        {result.fixed_code && (
          <div className="bg-slate-900 rounded-lg border border-slate-700 overflow-hidden">
            <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-700">
              <Code size={20} className="text-indigo-500" />
              <h3 className="font-semibold text-white">Fixed Code</h3>
            </div>
            <div className="p-4">
              <Editor
                height="300px"
                defaultLanguage="python"
                theme="vs-dark"
                value={result.fixed_code}
                options={{
                  readOnly: true,
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                }}
              />
            </div>
          </div>
        )}        
      </div>
    </div>
  );
};

export default Result;