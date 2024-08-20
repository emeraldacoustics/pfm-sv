import './App.css';
import Product from './components/product';
import Population from './components/population';

function App() {
  return (
    <div className="bg-gray-200 h-screen flex items-center justify-center">
      <div className='flex justify-around w-full'>
        <Product />
        <Population />
      </div>
    </div>
  );
}

export default App;
