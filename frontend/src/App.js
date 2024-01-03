import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './utils/ProtectedRoute';
import Login from './views/Login';
import Register from './views/Register';
import Dashboard from './views/Dashboard';
import { Toaster } from 'react-hot-toast';
import NavBar from './components/Navbar/NavBar';
import MyTrip from './views/myTrip';

function App() {
  return (
    <div className="App">
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <div>
                  <ProtectedRoute>
                    {' '}
                    <NavBar />
                    <Dashboard />{' '}
                  </ProtectedRoute>
                </div>
              }
            />
            <Route
              path="/myTrip"
              element={
                <ProtectedRoute>
                  {' '}
                  <NavBar />
                  <MyTrip />{' '}
                </ProtectedRoute>
              }
            ></Route>
          </Routes>
          <Toaster />
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
