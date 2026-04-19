import { useState } from 'react'
import Header from './components/Header.jsx'
import CodeEditor from './components/CodeEditor.jsx'
import Result from './components/Result.jsx'
import { debugCode } from './services/api.js'  // Import API function

const App = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);  // Track errors

  const handleDebug = async (code) => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    
    try {
      // Call REAL API
      const response = await debugCode(code, 'python');
      console.log("API Response:", response);
      setResult(response);
    } catch (err) {
      console.error("API Error:", err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <Header />
      
      <main className="container mx-auto p-8">
        <div className="max-w-7xl mx-auto">
          {/* Show error message if API fails */}
          {error && (
            <div className="mb-6 bg-red-950/50 border border-red-500 text-red-300 px-4 py-3 rounded-lg">
              <p className="font-semibold">Error:</p>
              <p>{error}</p>
            </div>
          )}
          
          {/* Two column grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CodeEditor 
              onDebug={handleDebug}
              isLoading={isLoading}
            />
            
            <Result result={result} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App