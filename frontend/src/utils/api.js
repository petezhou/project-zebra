const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Fetch wrapper that automatically refreshes access token on 401.
 *
 * Uses sliding window refresh tokens:
 * - Access token expires in 30 min
 * - When expired, automatically calls /auth/refresh
 * - Refresh token in httpOnly cookie (7 days, sliding)
 * - Retries original request with new token
 */
export async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('access_token');

  // Add Authorization header if token exists
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Make request
  let response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers,
    credentials: 'include', // Important: send cookies (refresh token)
  });

  // If 401 (token expired), try to refresh
  if (response.status === 401 && token) {
    const refreshed = await refreshAccessToken();

    if (refreshed) {
      // Retry original request with new token
      const newToken = localStorage.getItem('access_token');
      headers['Authorization'] = `Bearer ${newToken}`;

      response = await fetch(`${API_URL}${url}`, {
        ...options,
        headers,
        credentials: 'include',
      });
    } else {
      // Refresh failed, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
      throw new Error('Session expired');
    }
  }

  return response;
}

/**
 * Refresh access token using refresh token (sliding window).
 * Returns true if successful, false otherwise.
 */
async function refreshAccessToken() {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include', // Send httpOnly refresh token cookie
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      return true;
    }

    return false;
  } catch (error) {
    console.error('Token refresh failed:', error);
    return false;
  }
}

/**
 * Logout - clear access token and call logout endpoint.
 */
export async function logout() {
  try {
    // Call backend to clear refresh token cookie
    await fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    });
  } catch (error) {
    console.error('Logout request failed:', error);
  } finally {
    // Always clear local token
    localStorage.removeItem('access_token');
  }
}
