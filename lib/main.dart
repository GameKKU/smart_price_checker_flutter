import 'package:flutter/material.dart';
import 'router/app_router.dart';

void main() {
  runApp(const SmartPriceCheckerApp());
}

class SmartPriceCheckerApp extends StatelessWidget {
  const SmartPriceCheckerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: '2nd Hand Price Checker',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.light,
        ),
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
          backgroundColor: Colors.white,
          foregroundColor: Colors.black87,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        cardTheme: CardTheme(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
      routerConfig: AppRouter.router,
    );
  }
}
