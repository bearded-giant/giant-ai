/**
 * Example target pattern for consistent error handling
 * Use with: ai-pattern-refactor refactor "error handling" --target-pattern patterns/error-handling-consistent.js
 */

// Consistent error handling pattern with logging
async function exampleOperation() {
  try {
    // Main operation logic
    const result = await performOperation();
    
    // Success logging
    logger.info('Operation completed successfully', {
      operationId: result.id,
      timestamp: new Date().toISOString()
    });
    
    return {
      success: true,
      data: result
    };
  } catch (error) {
    // Structured error logging
    logger.error('Operation failed', {
      error: error.message,
      stack: error.stack,
      context: {
        // Include relevant context
      }
    });
    
    // Re-throw with consistent error structure
    throw new AppError({
      code: error.code || 'OPERATION_FAILED',
      message: error.message,
      statusCode: error.statusCode || 500,
      originalError: error
    });
  }
}

// Custom error class for consistency
class AppError extends Error {
  constructor({ code, message, statusCode, originalError }) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
    this.originalError = originalError;
    Error.captureStackTrace(this, this.constructor);
  }
}