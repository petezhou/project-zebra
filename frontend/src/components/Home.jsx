import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiFetch, logout as apiLogout } from '../utils/api';
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

      // apiFetch automatically refreshes token if expired
      const response = await apiFetch('/auth/me');

      if (!response.ok) {
        // If still failing after refresh attempt, redirect to login
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

  const handleLogout = async () => {
    await apiLogout(); // Clears refresh token cookie on backend
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
