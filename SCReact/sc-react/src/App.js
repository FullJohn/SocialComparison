import logo from './logo.svg';
import './App.css';

import {Home} from './Home';
import {Post} from './Post';
import {Navigation} from './Navigation';

import {BrowserRouter, Route, Routes} from 'react-router-dom';
import { LoadScreen } from './LoadingScreen';

function App() {
  return (
    <BrowserRouter>
    <div className="container">
      <h3 className = "m-3 d-flex justify-content-center">
        Brand Comparison
      </h3>

      <Navigation/>

      <Routes>
          <Route path='/home' element={<Home/>} />
          <Route path='/post' element={<Post/>} />
          <Route path='/loading' element={<LoadScreen/>} />

      </Routes>
    </div>
    </BrowserRouter>
  );
}

export default App;
