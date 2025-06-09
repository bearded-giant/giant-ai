/**
 * Example target pattern for modern async/await usage
 * Use with: ai-pattern-refactor refactor "promise chains" --target-pattern patterns/async-await-pattern.js
 */

// Modern async/await pattern instead of promise chains
async function fetchUserData(userId) {
  try {
    // Parallel operations when possible
    const [user, preferences, permissions] = await Promise.all([
      fetchUser(userId),
      fetchUserPreferences(userId),
      fetchUserPermissions(userId)
    ]);
    
    // Sequential operations when dependent
    const profile = await buildUserProfile(user);
    const enrichedProfile = await enrichProfile(profile, preferences);
    
    return {
      ...enrichedProfile,
      permissions,
      lastUpdated: new Date().toISOString()
    };
  } catch (error) {
    logger.error('Failed to fetch user data', { userId, error });
    throw new Error(`Unable to fetch data for user ${userId}`);
  }
}

// Utility function with proper error handling
async function retryOperation(operation, maxRetries = 3, delay = 1000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }
      
      logger.warn(`Operation failed, retrying (${attempt}/${maxRetries})`, { error });
      await new Promise(resolve => setTimeout(resolve, delay * attempt));
    }
  }
}