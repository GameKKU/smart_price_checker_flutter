import 'package:flutter/material.dart';
import 'router/app_router.dart';

void main() {
  runApp(const BarterGangApp());
}

class BarterGangApp extends StatelessWidget {
  const BarterGangApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Barter Gang App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.pink,
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFFFC000),
          brightness: Brightness.light,
        ).copyWith(
          background: const Color(0xFFFFC000).withOpacity(0.4),
          surface: const Color(0xFFFFC000).withOpacity(0.3),
        ),
        appBarTheme: AppBarTheme(
          centerTitle: true,
          elevation: 0,
          backgroundColor: const Color(0xFFFFC000).withOpacity(0.6),
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
