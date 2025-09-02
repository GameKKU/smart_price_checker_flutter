class ItemInfo {
  final String name;
  final String series;
  final String year;
  final String condition;

  ItemInfo({
    required this.name,
    required this.series,
    required this.year,
    required this.condition,
  });

  factory ItemInfo.fromJson(Map<String, dynamic> json) {
    return ItemInfo(
      name: json['name'] ?? '',
      series: json['series'] ?? '',
      year: json['year'] ?? '',
      condition: json['condition'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'series': series,
      'year': year,
      'condition': condition,
    };
  }
}

class PriceRange {
  final double min;
  final double max;
  final String currency;
  final double suggested;

  PriceRange({
    required this.min,
    required this.max,
    required this.currency,
    required this.suggested,
  });

  String get formattedSuggested {
    return '${suggested.toStringAsFixed(0)} $currency';
  }

  String get formattedRange {
    return '${min.toStringAsFixed(0)} - ${max.toStringAsFixed(0)} $currency';
  }

  factory PriceRange.fromJson(Map<String, dynamic> json) {
    return PriceRange(
      min: (json['min'] ?? 0).toDouble(),
      max: (json['max'] ?? 0).toDouble(),
      currency: json['currency'] ?? 'USD',
      suggested: (json['suggested'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'min': min,
      'max': max,
      'currency': currency,
      'suggested': suggested,
    };
  }
}

class MarketResult {
  final String title;
  final String price;
  final String source;
  final String? url;

  MarketResult({
    required this.title,
    required this.price,
    required this.source,
    this.url,
  });

  factory MarketResult.fromJson(Map<String, dynamic> json) {
    return MarketResult(
      title: json['title'] ?? '',
      price: json['price'] ?? '',
      source: json['source'] ?? '',
      url: json['url'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'price': price,
      'source': source,
      'url': url,
    };
  }
}

class AnalysisResponse {
  final String analysisId;
  final String status;
  final int estimatedTime;

  AnalysisResponse({
    required this.analysisId,
    required this.status,
    required this.estimatedTime,
  });

  factory AnalysisResponse.fromJson(Map<String, dynamic> json) {
    return AnalysisResponse(
      analysisId: json['analysis_id'] ?? '',
      status: json['status'] ?? '',
      estimatedTime: json['estimated_time'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'analysis_id': analysisId,
      'status': status,
      'estimated_time': estimatedTime,
    };
  }
}

class AnalysisResult {
  final String analysisId;
  final String status;
  final ItemInfo? itemInfo;
  final PriceRange? priceRange;
  final double? confidence;
  final List<MarketResult> marketData;
  final DateTime createdAt;
  final DateTime? completedAt;
  final String? errorMessage;

  AnalysisResult({
    required this.analysisId,
    required this.status,
    this.itemInfo,
    this.priceRange,
    this.confidence,
    required this.marketData,
    required this.createdAt,
    this.completedAt,
    this.errorMessage,
  });

  factory AnalysisResult.fromJson(Map<String, dynamic> json) {
    return AnalysisResult(
      analysisId: json['analysis_id'] ?? '',
      status: json['status'] ?? '',
      itemInfo: json['item_info'] != null 
          ? ItemInfo.fromJson(json['item_info']) 
          : null,
      priceRange: json['price_range'] != null 
          ? PriceRange.fromJson(json['price_range']) 
          : null,
      confidence: json['confidence']?.toDouble(),
      marketData: (json['market_data'] as List<dynamic>? ?? [])
          .map((item) => MarketResult.fromJson(item))
          .toList(),
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at']) 
          : null,
      errorMessage: json['error_message'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'analysis_id': analysisId,
      'status': status,
      'item_info': itemInfo?.toJson(),
      'price_range': priceRange?.toJson(),
      'confidence': confidence,
      'market_data': marketData.map((item) => item.toJson()).toList(),
      'created_at': createdAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'error_message': errorMessage,
    };
  }
}

class UserHistoryResponse {
  final List<AnalysisResult> analyses;
  final int totalCount;
  final int page;
  final int limit;

  UserHistoryResponse({
    required this.analyses,
    required this.totalCount,
    required this.page,
    required this.limit,
  });

  factory UserHistoryResponse.fromJson(Map<String, dynamic> json) {
    return UserHistoryResponse(
      analyses: (json['analyses'] as List<dynamic>? ?? [])
          .map((item) => AnalysisResult.fromJson(item))
          .toList(),
      totalCount: json['total_count'] ?? 0,
      page: json['page'] ?? 1,
      limit: json['limit'] ?? 20,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'analyses': analyses.map((item) => item.toJson()).toList(),
      'total_count': totalCount,
      'page': page,
      'limit': limit,
    };
  }
}