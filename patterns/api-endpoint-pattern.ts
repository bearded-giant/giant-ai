/**
 * Example target pattern for consistent API endpoints (TypeScript)
 * Use with: ai-pattern-refactor refactor "API endpoints" --target-pattern patterns/api-endpoint-pattern.ts
 */

import { Request, Response, NextFunction } from 'express';
import { validate } from '../middleware/validation';
import { authenticate } from '../middleware/auth';
import { ApiResponse, ApiError } from '../types/api';

// Consistent API endpoint pattern
export const createUserEndpoint = {
  // Route configuration
  path: '/api/v1/users',
  method: 'POST',
  
  // Middleware stack
  middleware: [
    authenticate(),
    validate(createUserSchema)
  ],
  
  // Main handler with proper typing
  handler: async (
    req: Request<{}, {}, CreateUserDto>,
    res: Response<ApiResponse<User>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      // Input validation is handled by middleware
      const userData = req.body;
      
      // Business logic in service layer
      const user = await userService.createUser(userData);
      
      // Consistent response format
      res.status(201).json({
        success: true,
        data: user,
        metadata: {
          timestamp: new Date().toISOString(),
          version: 'v1'
        }
      });
    } catch (error) {
      // Error handling delegated to error middleware
      next(error);
    }
  }
};

// Validation schema
const createUserSchema = {
  body: {
    type: 'object',
    required: ['email', 'name'],
    properties: {
      email: { type: 'string', format: 'email' },
      name: { type: 'string', minLength: 2 },
      role: { type: 'string', enum: ['user', 'admin'] }
    }
  }
};