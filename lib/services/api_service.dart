import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:http_parser/http_parser.dart';
import '../models/models.dart';

class ApiService {
  static const String _baseUrl = 'http://10.0.2.2:8001';
  late final Dio _dio;

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: _baseUrl,
      connectTimeout: 30000, // 30 seconds in milliseconds
      receiveTimeout: 30000, // 30 seconds in milliseconds
      headers: {
        'Content-Type': 'application/json',
      },
    ));

    // Add interceptors for logging
    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
      logPrint: (obj) => print(obj),
    ));
  }

  /// Upload images for analysis
  Future<AnalysisResponse> analyzeImages(
    List<File> images, {
    String? userId,
  }) async {
    try {
      final formData = FormData();

      // Add images to form data
      for (int i = 0; i < images.length; i++) {
        final file = images[i];
        
        // Determine content type based on file extension
        String contentType = 'image/jpeg'; // default
        String filename = 'image_$i.jpg'; // default
        
        final extension = file.path.toLowerCase().split('.').last;
        switch (extension) {
          case 'jpg':
          case 'jpeg':
            contentType = 'image/jpeg';
            filename = 'image_$i.jpg';
            break;
          case 'png':
            contentType = 'image/png';
            filename = 'image_$i.png';
            break;
          case 'gif':
            contentType = 'image/gif';
            filename = 'image_$i.gif';
            break;
          case 'webp':
            contentType = 'image/webp';
            filename = 'image_$i.webp';
            break;
        }
        
        formData.files.add(MapEntry(
          'images',
          await MultipartFile.fromFile(
            file.path,
            filename: filename,
            contentType: MediaType.parse(contentType),
          ),
        ));
      }

      // Add user ID if provided
      if (userId != null) {
        formData.fields.add(MapEntry('user_id', userId));
      }

      final response = await _dio.post(
        '/api/analyze',
        data: formData,
      );

      return AnalysisResponse.fromJson(response.data);
    } on DioError catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw Exception('Failed to analyze images: $e');
    }
  }

  /// Get analysis result by ID
  Future<AnalysisResult> getAnalysis(String analysisId) async {
    try {
      final response = await _dio.get('/api/analysis/$analysisId');
      return AnalysisResult.fromJson(response.data);
    } on DioError catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw Exception('Failed to get analysis: $e');
    }
  }

  /// Get user history
  Future<UserHistoryResponse> getUserHistory(
    String userId, {
    int page = 1,
    int limit = 20,
  }) async {
    try {
      final response = await _dio.get(
        '/api/history/$userId',
        queryParameters: {
          'page': page,
          'limit': limit,
        },
      );
      return UserHistoryResponse.fromJson(response.data);
    } on DioError catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw Exception('Failed to get user history: $e');
    }
  }

  /// Delete analysis
  Future<void> deleteAnalysis(String analysisId) async {
    try {
      await _dio.delete('/api/analysis/$analysisId');
    } on DioError catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw Exception('Failed to delete analysis: $e');
    }
  }

  /// Health check
  Future<bool> healthCheck() async {
    try {
      final response = await _dio.get('/');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Handle Dio errors
  Exception _handleDioError(DioError e) {
    switch (e.type) {
      case DioErrorType.connectTimeout:
      case DioErrorType.sendTimeout:
      case DioErrorType.receiveTimeout:
        return Exception('Connection timeout. Please check your internet connection.');
      case DioErrorType.response:
        final statusCode = e.response?.statusCode;
        final message = e.response?.data?['detail'] ?? 'Unknown error occurred';
        return Exception('Server error ($statusCode): $message');
      case DioErrorType.cancel:
        return Exception('Request was cancelled');
      case DioErrorType.other:
        return Exception('No internet connection. Please check your network.');
      default:
        return Exception('Network error: ${e.message}');
    }
  }
}

// Singleton instance
final apiService = ApiService();