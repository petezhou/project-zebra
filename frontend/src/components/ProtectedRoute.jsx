import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token')

  if (!token) {
    // Not authenticated, redirect to login
    return <Navigate to="/login" replace />
  }

  return children
}
