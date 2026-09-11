import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState<number>(0)

  return (
    <main className="app">
      <h1>PC Club</h1>
      <p>React + Vite + TypeScript — фронтенд готов к разработке.</p>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          Проверка интерактивности: {count}
        </button>
        <p>
          Отредактируйте <code>src/App.tsx</code> — HMR подхватит изменения
          без перезагрузки страницы.
        </p>
      </div>
    </main>
  )
}

export default App
