import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

export default function Home() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        navigate('/login');
        return;
      }

      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        // Token expired or invalid
        localStorage.removeItem('access_token');
        navigate('/login');
        return;
      }

      const data = await response.json();
      setUser(data);
    } catch (err) {
      console.error('Error fetching user:', err);
      navigate('/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="container">
        <div className="form-card">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="form-card">
        <h1>Hi {user?.full_name}</h1>
        <button onClick={handleLogout} style={{ marginTop: '24px' }}>
          Sign out
        </button>
      </div>
    </div>
  );
}
